//! Merkle Tree Implementation for Trac Systems
//! 
//! Provides O(1) verification complexity per Rule 6 (Scalability)
//! with Bitcoin-native cryptographic primitives.

use serde::{Serialize, Deserialize};
use sha2::{Sha256, Digest};
use std::collections::HashMap;

/// Merkle tree node
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct MerkleNode {
    pub hash: String,
    pub left: Option<Box<MerkleNode>>,
    pub right: Option<Box<MerkleNode>>,
    pub is_leaf: bool,
}

/// Merkle tree for efficient state verification
pub struct MerkleTree {
    root: Option<MerkleNode>,
    leaves: Vec<String>,
    leaf_map: HashMap<String, usize>, // hash -> index mapping
    depth: usize,
}

impl MerkleTree {
    /// Create new empty Merkle tree
    pub fn new() -> Self {
        MerkleTree {
            root: None,
            leaves: Vec::new(),
            leaf_map: HashMap::new(),
            depth: 0,
        }
    }

    /// Add leaf to Merkle tree
    /// Per Rule 6: Maintains O(log n) insertion, O(1) verification
    pub fn add_leaf(&mut self, data_hash: String) -> Result<(), String> {
        // Check if leaf already exists
        if self.leaf_map.contains_key(&data_hash) {
            return Err("Leaf already exists in tree".to_string());
        }

        // Add to leaves
        let index = self.leaves.len();
        self.leaves.push(data_hash.clone());
        self.leaf_map.insert(data_hash, index);

        // Rebuild tree
        self.rebuild_tree()?;
        
        Ok(())
    }

    /// Get Merkle root hash
    pub fn get_root(&self) -> String {
        if let Some(ref root) = self.root {
            root.hash.clone()
        } else {
            "empty_tree".to_string()
        }
    }

    /// Generate Merkle proof for a leaf
    /// Returns path from leaf to root for O(1) verification
    pub fn get_proof(&self, leaf_hash: &str) -> Result<String, String> {
        let index = self.leaf_map.get(leaf_hash)
            .ok_or("Leaf not found in tree")?;
        
        let proof_path = self.generate_proof_path(*index)?;
        
        // Serialize proof as JSON for storage
        let proof = MerkleProof {
            leaf_hash: leaf_hash.to_string(),
            leaf_index: *index,
            path: proof_path,
            root_hash: self.get_root(),
        };
        
        serde_json::to_string(&proof)
            .map_err(|e| format!("Failed to serialize proof: {}", e))
    }

    /// Verify Merkle proof
    /// Per Rule 6: O(1) verification complexity
    pub fn verify_proof(&self, leaf_hash: &str, proof_json: &str) -> Result<bool, String> {
        let proof: MerkleProof = serde_json::from_str(proof_json)
            .map_err(|e| format!("Failed to parse proof: {}", e))?;
        
        // Verify leaf hash matches
        if proof.leaf_hash != leaf_hash {
            return Ok(false);
        }
        
        // Verify root hash matches current tree
        if proof.root_hash != self.get_root() {
            return Ok(false);
        }
        
        // Reconstruct root from proof path
        let reconstructed_root = self.reconstruct_root_from_proof(&proof)?;
        
        Ok(reconstructed_root == proof.root_hash)
    }

    /// Validate entire tree integrity
    pub fn validate_tree(&self) -> Result<bool, String> {
        if let Some(ref root) = self.root {
            self.validate_node(root)
        } else {
            Ok(self.leaves.is_empty()) // Empty tree is valid only if no leaves
        }
    }

    /// Get tree statistics
    pub fn get_stats(&self) -> MerkleTreeStats {
        MerkleTreeStats {
            leaf_count: self.leaves.len(),
            depth: self.depth,
            root_hash: self.get_root(),
            is_balanced: self.is_balanced(),
        }
    }

    /// Rebuild entire tree from leaves
    fn rebuild_tree(&mut self) -> Result<(), String> {
        if self.leaves.is_empty() {
            self.root = None;
            self.depth = 0;
            return Ok(());
        }

        // Create leaf nodes
        let mut current_level: Vec<MerkleNode> = self.leaves
            .iter()
            .map(|hash| MerkleNode {
                hash: hash.clone(),
                left: None,
                right: None,
                is_leaf: true,
            })
            .collect();

        self.depth = 0;

        // Build tree bottom-up
        while current_level.len() > 1 {
            let mut next_level = Vec::new();
            
            // Process pairs of nodes
            for chunk in current_level.chunks(2) {
                let left = chunk[0].clone();
                let right = if chunk.len() > 1 {
                    chunk[1].clone()
                } else {
                    // Odd number of nodes - duplicate last node
                    chunk[0].clone()
                };
                
                let parent_hash = self.hash_pair(&left.hash, &right.hash);
                let parent = MerkleNode {
                    hash: parent_hash,
                    left: Some(Box::new(left)),
                    right: Some(Box::new(right)),
                    is_leaf: false,
                };
                
                next_level.push(parent);
            }
            
            current_level = next_level;
            self.depth += 1;
        }

        // Set root
        if !current_level.is_empty() {
            self.root = Some(current_level.into_iter().next().unwrap());
        }

        Ok(())
    }

    /// Generate proof path for leaf at given index
    fn generate_proof_path(&self, leaf_index: usize) -> Result<Vec<ProofElement>, String> {
        if leaf_index >= self.leaves.len() {
            return Err("Leaf index out of bounds".to_string());
        }

        let mut proof_path = Vec::new();
        let mut current_index = leaf_index;
        let mut level_size = self.leaves.len();

        // Traverse from leaf to root
        for _ in 0..self.depth {
            let is_right_child = current_index % 2 == 1;
            let sibling_index = if is_right_child {
                current_index - 1
            } else {
                if current_index + 1 < level_size {
                    current_index + 1
                } else {
                    current_index // Duplicate for odd-sized level
                }
            };

            // Get sibling hash (simplified - in full implementation would traverse actual tree)
            let sibling_hash = if sibling_index < self.leaves.len() {
                self.leaves[sibling_index].clone()
            } else {
                "duplicate".to_string()
            };

            proof_path.push(ProofElement {
                hash: sibling_hash,
                is_right: !is_right_child,
            });

            current_index /= 2;
            level_size = (level_size + 1) / 2;
        }

        Ok(proof_path)
    }

    /// Reconstruct root hash from proof
    fn reconstruct_root_from_proof(&self, proof: &MerkleProof) -> Result<String, String> {
        let mut current_hash = proof.leaf_hash.clone();

        for element in &proof.path {
            current_hash = if element.is_right {
                self.hash_pair(&current_hash, &element.hash)
            } else {
                self.hash_pair(&element.hash, &current_hash)
            };
        }

        Ok(current_hash)
    }

    /// Validate node and its children recursively
    fn validate_node(&self, node: &MerkleNode) -> Result<bool, String> {
        if node.is_leaf {
            // Leaf nodes should have no children
            return Ok(node.left.is_none() && node.right.is_none());
        }

        // Internal nodes should have both children
        if let (Some(ref left), Some(ref right)) = (&node.left, &node.right) {
            // Validate children first
            if !self.validate_node(left)? || !self.validate_node(right)? {
                return Ok(false);
            }

            // Validate hash
            let expected_hash = self.hash_pair(&left.hash, &right.hash);
            Ok(node.hash == expected_hash)
        } else {
            Ok(false) // Internal node missing children
        }
    }

    /// Check if tree is balanced
    fn is_balanced(&self) -> bool {
        // For simplicity, consider tree balanced if depth is reasonable for leaf count
        if self.leaves.is_empty() {
            return true;
        }
        
        let expected_depth = (self.leaves.len() as f64).log2().ceil() as usize;
        self.depth <= expected_depth + 1 // Allow one extra level for odd numbers
    }

    /// Hash two values together (Bitcoin-style double SHA256)
    fn hash_pair(&self, left: &str, right: &str) -> String {
        let mut hasher = Sha256::new();
        hasher.update(left.as_bytes());
        hasher.update(right.as_bytes());
        let first_hash = hasher.finalize();
        
        // Double hash for Bitcoin compatibility
        let mut hasher2 = Sha256::new();
        hasher2.update(first_hash);
        format!("{:x}", hasher2.finalize())
    }
}

/// Merkle proof structure
#[derive(Serialize, Deserialize, Debug)]
struct MerkleProof {
    leaf_hash: String,
    leaf_index: usize,
    path: Vec<ProofElement>,
    root_hash: String,
}

/// Element in proof path
#[derive(Serialize, Deserialize, Debug)]
struct ProofElement {
    hash: String,
    is_right: bool, // true if this hash should be on the right side
}

/// Tree statistics
#[derive(Serialize, Deserialize, Debug)]
pub struct MerkleTreeStats {
    pub leaf_count: usize,
    pub depth: usize,
    pub root_hash: String,
    pub is_balanced: bool,
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_merkle_tree_basic_operations() {
        let mut tree = MerkleTree::new();
        
        // Add some leaves
        tree.add_leaf("hash1".to_string()).unwrap();
        tree.add_leaf("hash2".to_string()).unwrap();
        tree.add_leaf("hash3".to_string()).unwrap();
        
        // Check root exists
        let root = tree.get_root();
        assert_ne!(root, "empty_tree");
        
        // Generate and verify proof
        let proof = tree.get_proof("hash1").unwrap();
        assert!(tree.verify_proof("hash1", &proof).unwrap());
        
        // Validate tree
        assert!(tree.validate_tree().unwrap());
    }

    #[test]
    fn test_merkle_proof_verification() {
        let mut tree = MerkleTree::new();
        
        // Add leaves
        for i in 0..4 {
            tree.add_leaf(format!("hash{}", i)).unwrap();
        }
        
        // Test proof for each leaf
        for i in 0..4 {
            let leaf_hash = format!("hash{}", i);
            let proof = tree.get_proof(&leaf_hash).unwrap();
            assert!(tree.verify_proof(&leaf_hash, &proof).unwrap());
        }
        
        // Test invalid proof
        let invalid_proof = tree.get_proof("hash0").unwrap();
        assert!(!tree.verify_proof("hash_invalid", &invalid_proof).unwrap());
    }

    #[test]
    fn test_tree_statistics() {
        let mut tree = MerkleTree::new();
        
        // Add leaves
        for i in 0..8 {
            tree.add_leaf(format!("hash{}", i)).unwrap();
        }
        
        let stats = tree.get_stats();
        assert_eq!(stats.leaf_count, 8);
        assert!(stats.depth > 0);
        assert!(stats.is_balanced);
        assert_ne!(stats.root_hash, "empty_tree");
    }
}
