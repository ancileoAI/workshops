# Instructions:
# 1. Set up pytest in your environment
# 2. Write tests for the provided classes
# 3. Practice using fixtures and parametrization
# 4. Run tests and check coverage

class StringProcessor:
    def __init__(self, default_separator=" "):
        self.default_separator = default_separator
        self.operation_count = 0
    
    def reverse_words(self, text):
        if not isinstance(text, str):
            raise TypeError("Input must be a string")
        
        if not text.strip():
            return ""
        
        self.operation_count += 1
        words = text.split(self.default_separator)
        return self.default_separator.join(reversed(words))
    
    def count_vowels(self, text):
        if not isinstance(text, str):
            raise TypeError("Input must be a string")
        
        self.operation_count += 1
        vowels = "aeiouAEIOU"
        return sum(1 for char in text if char in vowels)
    
    def truncate(self, text, max_length, suffix="..."):
        """Truncate text to max_length, adding suffix if truncated"""
        if not isinstance(text, str):
            raise TypeError("Input must be a string")
        
        if max_length < 0:
            raise ValueError("max_length must be non-negative")
        
        if len(suffix) > max_length:
            raise ValueError("Suffix cannot be longer than max_length")
        
        self.operation_count += 1
        
        if len(text) <= max_length:
            return text
        
        return text[:max_length - len(suffix)] + suffix
    
    def reset_counter(self):
        self.operation_count = 0


class WordCounter:
    """Count word frequency in text"""
    
    def __init__(self, case_sensitive=False):
        self.case_sensitive = case_sensitive
    
    def count_words(self, text):
        """Return a dictionary of word frequencies"""
        if not isinstance(text, str):
            raise TypeError("Input must be a string")
        
        if not text.strip():
            return {}
        
        # Process text based on case sensitivity
        processed_text = text if self.case_sensitive else text.lower()
        
        # Split into words and count
        words = processed_text.split()
        word_count = {}
        
        for word in words:
            # Remove punctuation from word
            clean_word = ''.join(char for char in word if char.isalnum())
            if clean_word:  # Only count non-empty words
                word_count[clean_word] = word_count.get(clean_word, 0) + 1
        
        return word_count
    
    def get_most_common(self, text, n=1):
        """Get the n most common words"""
        word_counts = self.count_words(text)
        if not word_counts:
            return []
        
        sorted_words = sorted(word_counts.items(), 
                            key=lambda x: (-x[1], x[0]))
        
        return sorted_words[:n]


# TODO Write tests using fixtures
class TestStringProcessorWithFixtures:
    
    @pytest.fixture
    def processor(self):
        # TODO: Create a fixture that returns a StringProcessor instance
        pass
    
    @pytest.fixture
    def sample_text(self):
        # TODO: Create a fixture with sample text for testing
        pass
    
    def test_with_fixtures(self, processor, sample_text):
        # TODO: Write a test using both fixtures
        pass

# TODO 3: Write parametrized tests
class TestStringProcessorParametrized:
    
    @pytest.mark.parametrize("input_text,expected", [
        # TODO: Add test cases for reverse_words
        # Format: (input, expected_output)
    ])
    def test_reverse_words_parametrized(self, input_text, expected):
        pass
    
    @pytest.mark.parametrize("text,expected_count", [
        # TODO: Add test cases for count_vowels
    ])
    def test_count_vowels_parametrized(self, text, expected_count):
        pass
    
    @pytest.mark.parametrize("text,max_len,expected", [
        # TODO: Add test cases for truncate
    ])
    def test_truncate_parametrized(self, text, max_len, expected):
        pass

# TODO: Integration tests
class TestIntegration:
    
    def test_processor_and_counter_together(self):
        # TODO: Write a test that uses both classes together
        # Example: Process text with StringProcessor, then count words
        pass

# ============================================================================
# BONUS CHALLENGES (if you finish early)
# ============================================================================

class TestBonusChallenges:
    
    def test_performance_with_large_text(self):
        # TODO: Test with very large text (10,000+ words)
        # Verify it completes in reasonable time
        pass
    
    def test_unicode_handling(self):
        # TODO: Test with unicode characters, emojis, etc.
        pass
    
    @pytest.mark.slow
    def test_memory_usage(self):
        # TODO: Test memory usage doesn't grow excessively
        # (This is an example of using custom markers)
        pass
