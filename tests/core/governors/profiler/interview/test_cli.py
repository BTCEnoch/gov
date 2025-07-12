"""Tests for the governor interview CLI"""

import pytest
import json
from pathlib import Path
import logging
from datetime import datetime
from unittest.mock import patch, MagicMock

from core.governors.profiler.interview.cli import process_governors
from core.governors.profiler.schemas.profile_schemas import GovernorProfile
from core.governors.traits.schemas.trait_schemas import VisualTraits

@pytest.fixture
def mock_args():
    """Create mock command line arguments"""
    args = MagicMock()
    args.profiles_dir = "/test/profiles"
    args.output_dir = "/test/output"
    args.knowledge_base = "/test/kb"
    args.max_concurrent = 2
    args.governor_filter = None
    return args

@pytest.fixture
def test_governors():
    """Create test governor profiles"""
    now = datetime.now()
    return [
        GovernorProfile(
            id="TEST1",
            name="Test Governor 1",
            rank=1,
            attributes=[],
            created_at=now,
            updated_at=now
        ),
        GovernorProfile(
            id="TEST2",
            name="Test Governor 2",
            rank=2,
            attributes=[],
            created_at=now,
            updated_at=now
        )
    ]

@pytest.fixture
def mock_processor():
    """Create mock BatchInterviewProcessor"""
    processor = MagicMock()
    processor.process_governors.return_value = {
        "TEST1": VisualTraits(
            form_type="geometric",
            color_scheme="AZURE",
            sacred_geometry=["SPIRAL"],
            manifestation="test",
            effects=["glow"]
        ),
        "TEST2": VisualTraits(
            form_type="organic",
            color_scheme="GOLDEN",
            sacred_geometry=["FLOWER_OF_LIFE"],
            manifestation="test",
            effects=["pulse"]
        )
    }
    return processor

@pytest.mark.asyncio
async def test_process_governors_success(
    mock_args,
    test_governors,
    mock_processor,
    tmp_path
):
    """Test successful processing of governors"""
    # Set up temporary directories
    mock_args.output_dir = str(tmp_path)
    
    # Mock processor
    with patch(
        "core.governors.profiler.interview.cli.BatchInterviewProcessor",
        return_value=mock_processor
    ):
        # Mock load_governor_profiles
        mock_processor.load_governor_profiles.return_value = test_governors
        
        # Run processing
        success = await process_governors(mock_args)
        
        assert success
        assert mock_processor.process_governors.called
        assert mock_processor.save_results.called
        
        # Check summary file
        summary_path = tmp_path / "processing_summary.json"
        assert summary_path.exists()
        
        with open(summary_path) as f:
            summary = json.load(f)
            assert summary["total_governors"] == 2
            assert summary["processed"] == 2
            assert summary["success_rate"] == 100.0

@pytest.mark.asyncio
async def test_process_governors_with_filter(
    mock_args,
    test_governors,
    mock_processor
):
    """Test processing with governor filter"""
    mock_args.governor_filter = "TEST1"
    
    with patch(
        "core.governors.profiler.interview.cli.BatchInterviewProcessor",
        return_value=mock_processor
    ):
        mock_processor.load_governor_profiles.return_value = test_governors
        
        success = await process_governors(mock_args)
        
        assert success
        processed_governors = mock_processor.process_governors.call_args[0][0]
        assert len(processed_governors) == 1
        assert processed_governors[0].id == "TEST1"

@pytest.mark.asyncio
async def test_process_governors_no_profiles(mock_args, mock_processor):
    """Test handling when no profiles are found"""
    with patch(
        "core.governors.profiler.interview.cli.BatchInterviewProcessor",
        return_value=mock_processor
    ):
        mock_processor.load_governor_profiles.return_value = []
        
        success = await process_governors(mock_args)
        
        assert not success
        assert not mock_processor.process_governors.called

@pytest.mark.asyncio
async def test_process_governors_error_handling(mock_args, mock_processor):
    """Test error handling during processing"""
    with patch(
        "core.governors.profiler.interview.cli.BatchInterviewProcessor",
        return_value=mock_processor
    ):
        mock_processor.process_governors.side_effect = Exception("Test error")
        now = datetime.now()
        mock_processor.load_governor_profiles.return_value = [
            GovernorProfile(
                id="TEST1",
                name="Test Governor",
                rank=1,
                attributes=[],
                created_at=now,
                updated_at=now
            )
        ]
        
        success = await process_governors(mock_args)
        
        assert not success 