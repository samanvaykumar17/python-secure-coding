1. CWE-79-Cross-Site-Scripting  
2. CWE-89-SQL-Injection  
3. CWE-352-Cross-Site-Request-Forgery  
4. CWE-862-Missing-Authorization  
5. CWE-787-Out-of-bounds-Write  
6. CWE-22-Path-Traversal  
7. CWE-416-Use-After-Free  
8. CWE-125-Out-of-bounds-Read  
9. CWE-78-OS-Command-Injection  
10. CWE-94-Code-Injection  
11. CWE-120-Classic-Buffer-Overflow  
12. CWE-434-Unrestricted-File-Upload  
13. CWE-476-Null-Pointer-Dereference  
14. CWE-121-Stack-Based-Buffer-Overflow  
15. CWE-502-Deserialization-of-Untrusted-Data  
16. CWE-122-Heap-Overflow  
17. CWE-863-Incorrect-Authorization  
18. CWE-20-Improper-Input-Validation  
19. CWE-284-Improper-Access-Control  
20. CWE-200-Information-Disclosure  
21. CWE-306-Missing-Authentication  
22. CWE-918-Server-Site-Request-Forgery  
23. CWE-77-Command-Injection  
24. CWE-639-Authorization-Bypass  
25. CWE-770-Resource-Allocation-Without-Limits  



├── INJECTION  
│   │
│   ├── CWE-77 Command Injection  
│   │   └── CWE-78 OS Command Injection  
│   │
│   ├── CWE-79 Cross-Site Scripting  
│   │
│   ├── CWE-89 SQL Injection  
│   │
│   └── CWE-94 Code Injection  
│
├── ACCESS CONTROL / AUTHENTICATION
│   │
│   ├── CWE-284 Improper Access Control
│   │   │
│   │   ├── CWE-862 Missing Authorization
│   │   │
│   │   └── CWE-863 Incorrect Authorization
│   │       │
│   │       └── CWE-639 Authorization Bypass
│   │
│   └── CWE-306 Missing Authentication
│
├── MEMORY SAFETY
│   │
│   ├── CWE-787 Out-of-bounds Write
│   │   │
│   │   └── CWE-120 Classic Buffer Overflow
│   │       ├── CWE-121 Stack based Buffer Overflow
│   │       └── CWE-122 Heap Overflow
│   │
│   ├── CWE-125 Out-of-bounds Read
│   │
│   ├── CWE-416 Use-After-Free
│   │
│   └── CWE-476 Null Pointer Dereference
│
├── INPUT / DATA HANDLING
│   │
│   ├── CWE-20 Improper Input Validation
│   ├── CWE-22 Path Traversal
│   ├── CWE-434 Unrestricted File Upload
│   └── CWE-502 Deserialization of Untrusted Data
│
├── WEB REQUEST / WEB SECURITY
│   │
│   ├── CWE-352 CSRF
│   └── CWE-918 SSRF
│
├── INFORMATION EXPOSURE
│   │
│   └── CWE-200 Information Disclosure
│
└── RESOURCE MANAGEMENT
    │
    └── CWE-770 Resource Allocation Without Limits
