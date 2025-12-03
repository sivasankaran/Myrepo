#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdarg.h>

// Debug logging levels
typedef enum {
    DEBUG_LEVEL_ERROR = 0,
    DEBUG_LEVEL_WARN = 1,
    DEBUG_LEVEL_INFO = 2,
    DEBUG_LEVEL_DEBUG = 3
} DebugLevel;

static DebugLevel currentLevel = DEBUG_LEVEL_INFO;

// Safe debug logging function
void debug_log(DebugLevel level, const char *format, ...) {
    if (level > currentLevel) {
        return;
    }
    
    const char *levelStr;
    switch (level) {
        case DEBUG_LEVEL_ERROR:
            levelStr = "[ERROR]";
            break;
        case DEBUG_LEVEL_WARN:
            levelStr = "[WARN]";
            break;
        case DEBUG_LEVEL_INFO:
            levelStr = "[INFO]";
            break;
        case DEBUG_LEVEL_DEBUG:
            levelStr = "[DEBUG]";
            break;
        default:
            levelStr = "[UNKNOWN]";
    }
    
    printf("%s ", levelStr);
    
    va_list args;
    va_start(args, format);
    vprintf(format, args);
    va_end(args);
    
    printf("\n");
}

// Safe example function with input validation
void safe_function(const char *user_input) {
    debug_log(DEBUG_LEVEL_DEBUG, "safe_function called");
    
    if (user_input == NULL) {
        debug_log(DEBUG_LEVEL_ERROR, "user_input is NULL");
        return;
    }
    
    char buffer[256];
    size_t input_len = strlen(user_input);
    
    if (input_len >= sizeof(buffer)) {
        debug_log(DEBUG_LEVEL_ERROR, "Input too long: %zu bytes", input_len);
        return;
    }
    
    // Safe string copy
    strncpy(buffer, user_input, sizeof(buffer) - 1);
    buffer[sizeof(buffer) - 1] = '\0';
    
    debug_log(DEBUG_LEVEL_INFO, "Processed input: %s", buffer);
}

// Safe query function with parameterization
void process_query_safe(const char *user_id) {
    debug_log(DEBUG_LEVEL_DEBUG, "process_query_safe called");
    
    if (user_id == NULL) {
        debug_log(DEBUG_LEVEL_ERROR, "user_id is NULL");
        return;
    }
    
    // Validate user_id contains only digits
    for (size_t i = 0; user_id[i] != '\0'; i++) {
        if (user_id[i] < '0' || user_id[i] > '9') {
            debug_log(DEBUG_LEVEL_ERROR, "Invalid user_id format");
            return;
        }
    }
    
    debug_log(DEBUG_LEVEL_INFO, "Query executed for user_id: %s", user_id);
}

// Removed vulnerable functions - replaced with safe versions above

int main(int argc, char *argv[]) {
    debug_log(DEBUG_LEVEL_INFO, "Application started with %d arguments", argc);
    
    // Set debug level
    currentLevel = DEBUG_LEVEL_DEBUG;
    
    if (argc > 1) {
        debug_log(DEBUG_LEVEL_DEBUG, "Processing argument: %s", argv[1]);
        safe_function(argv[1]);
        process_query_safe(argv[1]);
    } else {
        debug_log(DEBUG_LEVEL_WARN, "No arguments provided");
    }
    
    debug_log(DEBUG_LEVEL_INFO, "Application finished");
    return 0;
}