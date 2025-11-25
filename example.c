#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Example function with potential security issues for Snyk to detect
void vulnerable_function(char *user_input) {
    char buffer[10];
    // Issue: Buffer overflow risk
    strcpy(buffer, user_input);
    printf("Input: %s\n", buffer);
}

// Example function with SQL injection risk
void process_query(char *user_id) {
    char query[100];
    // Issue: SQL injection vulnerability
    sprintf(query, "SELECT * FROM users WHERE id = %s", user_id);
    printf("Query: %s\n", query);
}

// Safe example function
void safe_function(const char *user_input) {
    char buffer[256];
    if (user_input != NULL) {
        // Use safe string functions
        strncpy(buffer, user_input, sizeof(buffer) - 1);
        buffer[sizeof(buffer) - 1] = '\0';
        printf("Safe input: %s\n", buffer);
    }
}

int main(int argc, char *argv[]) {
    if (argc > 1) {
        vulnerable_function(argv[1]);
        process_query(argv[1]);
        safe_function(argv[1]);
    }
    return 0;
}