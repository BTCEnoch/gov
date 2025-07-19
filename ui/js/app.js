/**
 * Enochian Cyphers - Main Application Controller
 * Zero external dependencies - Pure JavaScript implementation
 * Coordinates all UI components and WASM integration
 */

class EnochianCyphersApp {
    constructor() {
        this.currentView = 'lighthouse';
        this.isInitialized = false;
        this.wasmModule = null;
        this.sacredData = {
            traditions: [],
            governors: [],
            quests: [],
            stats: {}
        };
        
        console.log('🔮 Enochian Cyphers App initializing...');
        this.init();
    }
    
    /**
     * Initialize the application
     */
    async init() {
        try {
            // Show loading screen
            this.showLoader();
            
            // Load WASM module
            await this.loadWasmModule();
            
            // Initialize sacred data
            await this.initializeSacredData();
            
            // Setup event listeners
            this.setupEventListeners();
            
            // Initialize UI components
            this.initializeUI();
            
            // Hide loader and show app
            this.hideLoader();
            
            this.isInitialized = true;
            console.log('✅ Enochian Cyphers App initialized successfully');
            
        } catch (error) {
            console.error('❌ App initialization failed:', error);
            this.showError('Failed to initialize Enochian Cyphers: ' + error.message);
        }
    }
    
    /**
     * Load WASM module
     */
    async loadWasmModule() {
        try {
            this.updateLoadingText('Loading Sacred Architecture...');
            this.wasmModule = await window.EnochianWasm.loadWasm();
            
            if (window.EnochianWasm.isFallbackMode()) {
                console.warn('🔮 Running in JavaScript fallback mode');
                this.updateLoadingText('Sacred Architecture loaded (JavaScript mode)');
            } else {
                this.updateLoadingText('Sacred Architecture loaded (WASM mode)');
            }
            
        } catch (error) {
            console.error('Failed to load WASM module:', error);
            throw new Error('Sacred Architecture loading failed');
        }
    }
    
    /**
     * Initialize sacred data from WASM/fallback
     */
    async initializeSacredData() {
        try {
            this.updateLoadingText('Invoking Sacred Knowledge...');
            
            // Initialize lighthouse
            const initResult = this.wasmModule.exports.initialize_lighthouse();
            if (!initResult) {
                throw new Error('Lighthouse initialization failed');
            }
            
            // Load sacred statistics
            const statsJson = this.wasmModule.exports.get_sacred_stats();
            this.sacredData.stats = JSON.parse(statsJson);
            
            // Load traditions data (mock for now)
            this.sacredData.traditions = await this.loadTraditionsData();
            
            // Load governors data (mock for now)
            this.sacredData.governors = await this.loadGovernorsData();
            
            this.updateLoadingText('Sacred Knowledge invoked successfully');
            
        } catch (error) {
            console.error('Failed to initialize sacred data:', error);
            throw new Error('Sacred Knowledge invocation failed');
        }
    }
    
    /**
     * Load traditions data
     */
    async loadTraditionsData() {
        // Mock data - would load from actual lighthouse in production
        return [
            { id: 'enochian_magic', name: 'Enochian Magic', category: 'magick_systems', entries: 120, priority: 'critical' },
            { id: 'hermetic_qabalah', name: 'Hermetic Qabalah', category: 'magick_systems', entries: 110, priority: 'critical' },
            { id: 'thelema', name: 'Thelema', category: 'magick_systems', entries: 105, priority: 'high' },
            { id: 'golden_dawn', name: 'Golden Dawn', category: 'magick_systems', entries: 108, priority: 'high' },
            { id: 'chaos_magic', name: 'Chaos Magic', category: 'magick_systems', entries: 95, priority: 'medium' },
            { id: 'alchemy', name: 'Alchemy', category: 'magick_systems', entries: 115, priority: 'high' },
            { id: 'celtic_druidic', name: 'Celtic Druidic', category: 'magick_systems', entries: 100, priority: 'medium' },
            { id: 'taoism', name: 'Taoism', category: 'philosophy', entries: 110, priority: 'high' },
            { id: 'sufism', name: 'Sufism', category: 'philosophy', entries: 105, priority: 'high' },
            { id: 'gnosticism', name: 'Gnosticism', category: 'philosophy', entries: 100, priority: 'medium' },
            { id: 'traditional_kabbalah', name: 'Traditional Kabbalah', category: 'philosophy', entries: 125, priority: 'high' },
            { id: 'greek_philosophy', name: 'Greek Philosophy', category: 'philosophy', entries: 90, priority: 'medium' },
            { id: 'vedic_traditions', name: 'Vedic Traditions', category: 'philosophy', entries: 95, priority: 'medium' },
            { id: 'tarot', name: 'Tarot', category: 'divination_systems', entries: 78, priority: 'high' },
            { id: 'i_ching', name: 'I Ching', category: 'divination_systems', entries: 64, priority: 'high' },
            { id: 'astrology', name: 'Astrology', category: 'divination_systems', entries: 120, priority: 'high' },
            { id: 'numerology', name: 'Numerology', category: 'divination_systems', entries: 85, priority: 'medium' },
            { id: 'norse_traditions', name: 'Norse Traditions', category: 'divination_systems', entries: 90, priority: 'medium' },
            { id: 'shamanism', name: 'Shamanism', category: 'divination_systems', entries: 110, priority: 'medium' },
            { id: 'quantum_physics', name: 'Quantum Physics', category: 'science_reality', entries: 100, priority: 'high' },
            { id: 'sacred_geometry', name: 'Sacred Geometry', category: 'science_reality', entries: 95, priority: 'high' },
            { id: 'digital_physics', name: 'Digital Physics', category: 'science_reality', entries: 80, priority: 'medium' },
            { id: 'm_theory', name: 'M-Theory', category: 'science_reality', entries: 75, priority: 'medium' },
            { id: 'egyptian_magic', name: 'Egyptian Magic', category: 'science_reality', entries: 105, priority: 'medium' },
            { id: 'greek_mythology', name: 'Greek Mythology', category: 'science_reality', entries: 85, priority: 'medium' },
            { id: 'kuji_kiri', name: 'Kuji-Kiri', category: 'science_reality', entries: 70, priority: 'low' }
        ];
    }
    
    /**
     * Load governors data
     */
    async loadGovernorsData() {
        // Mock data - would load from actual governor profiles in production
        const governors = [];
        const aethyrs = ['TEX', 'ARN', 'ZOM', 'PAZ', 'LIT', 'MAZ', 'DEO']; // Sample aethyrs
        
        for (let i = 1; i <= 91; i++) {
            const aethyr = aethyrs[Math.floor(Math.random() * aethyrs.length)];
            governors.push({
                id: i,
                name: `GOVERNOR_${i.toString().padStart(2, '0')}`,
                aethyr: aethyr,
                tier: aethyr === 'TEX' ? 'transcendence' : 'mastery',
                personality: 'Wise and contemplative',
                traditions: ['enochian_magic', 'hermetic_qabalah'],
                quests_generated: Math.floor(Math.random() * 100) + 25
            });
        }
        
        return governors;
    }
    
    /**
     * Setup event listeners
     */
    setupEventListeners() {
        // Navigation buttons
        document.querySelectorAll('.nav-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const view = e.target.dataset.view;
                this.switchView(view);
            });
        });
        
        // Error modal close
        const closeErrorBtn = document.getElementById('close-error');
        if (closeErrorBtn) {
            closeErrorBtn.addEventListener('click', () => {
                this.hideError();
            });
        }
        
        // Handle URL parameters
        this.handleUrlParams();
        
        // Handle browser back/forward
        window.addEventListener('popstate', () => {
            this.handleUrlParams();
        });
    }
    
    /**
     * Handle URL parameters for deep linking
     */
    handleUrlParams() {
        const params = new URLSearchParams(window.location.search);
        const view = params.get('view');
        const action = params.get('action');
        
        if (view && ['lighthouse', 'governors', 'quests', 'divination', 'bitcoin'].includes(view)) {
            this.switchView(view);
        }
        
        if (action === 'generate-quest') {
            this.switchView('quests');
            // Trigger quest generation after a short delay
            setTimeout(() => {
                const generateBtn = document.getElementById('generate-quest');
                if (generateBtn) generateBtn.click();
            }, 500);
        }
    }
    
    /**
     * Initialize UI components
     */
    initializeUI() {
        this.updateLoadingText('Initializing Sacred Interface...');
        
        // Update stats in footer
        this.updateSacredStats();
        
        // Initialize each view
        if (window.LighthouseUI) window.LighthouseUI.init(this.sacredData.traditions);
        if (window.GovernorsUI) window.GovernorsUI.init(this.sacredData.governors);
        if (window.QuestsUI) window.QuestsUI.init(this.wasmModule);
        if (window.DivinationUI) window.DivinationUI.init(this.wasmModule);
        if (window.BitcoinUI) window.BitcoinUI.init(this.wasmModule);
        
        // Set initial view
        this.switchView(this.currentView);
    }
    
    /**
     * Switch between views
     */
    switchView(viewName) {
        // Update navigation
        document.querySelectorAll('.nav-btn').forEach(btn => {
            btn.classList.remove('active');
            if (btn.dataset.view === viewName) {
                btn.classList.add('active');
            }
        });
        
        // Update content views
        document.querySelectorAll('.content-view').forEach(view => {
            view.classList.remove('active');
        });
        
        const targetView = document.getElementById(`${viewName}-view`);
        if (targetView) {
            targetView.classList.add('active');
            this.currentView = viewName;
            
            // Update URL without page reload
            const url = new URL(window.location);
            url.searchParams.set('view', viewName);
            window.history.pushState({}, '', url);
        }
    }
    
    /**
     * Update sacred statistics in footer
     */
    updateSacredStats() {
        const stats = this.sacredData.stats;
        
        const traditionCount = document.getElementById('tradition-count');
        const governorCount = document.getElementById('governor-count');
        const questCount = document.getElementById('quest-count');
        
        if (traditionCount) traditionCount.textContent = stats.traditions || 26;
        if (governorCount) governorCount.textContent = stats.governors || 91;
        if (questCount) questCount.textContent = stats.quests_generated || 0;
    }
    
    /**
     * Show loading screen
     */
    showLoader() {
        const loader = document.getElementById('sacred-loader');
        const app = document.getElementById('app');
        
        if (loader) loader.style.display = 'flex';
        if (app) app.style.display = 'none';
    }
    
    /**
     * Hide loading screen
     */
    hideLoader() {
        const loader = document.getElementById('sacred-loader');
        const app = document.getElementById('app');
        
        if (loader) {
            loader.style.opacity = '0';
            setTimeout(() => {
                loader.style.display = 'none';
            }, 500);
        }
        
        if (app) app.style.display = 'flex';
    }
    
    /**
     * Update loading text
     */
    updateLoadingText(text) {
        const loadingText = document.querySelector('.loading-text');
        if (loadingText) {
            loadingText.textContent = text;
        }
    }
    
    /**
     * Show error modal
     */
    showError(message) {
        const errorModal = document.getElementById('error-modal');
        const errorMessage = document.getElementById('error-message');
        
        if (errorModal && errorMessage) {
            errorMessage.textContent = message;
            errorModal.style.display = 'flex';
        }
    }
    
    /**
     * Hide error modal
     */
    hideError() {
        const errorModal = document.getElementById('error-modal');
        if (errorModal) {
            errorModal.style.display = 'none';
        }
    }
    
    /**
     * Get current sacred data
     */
    getSacredData() {
        return this.sacredData;
    }
    
    /**
     * Get WASM module
     */
    getWasmModule() {
        return this.wasmModule;
    }
    
    /**
     * Check if app is initialized
     */
    isReady() {
        return this.isInitialized;
    }
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.EnochianApp = new EnochianCyphersApp();
});

// Handle page visibility changes for PWA
document.addEventListener('visibilitychange', () => {
    if (document.visibilityState === 'visible' && window.EnochianApp) {
        console.log('🔮 App resumed');
        // Refresh connection status, sync data, etc.
    }
});
