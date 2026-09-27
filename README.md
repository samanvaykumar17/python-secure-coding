# Secure Coding Landscape   

## Types of Testing
We can do four types of automated vulnerability testing  

### SAST (Automatic, Static)  
It will look into your source code repository and find issues.  It will even give you the filename and line number of the problematic code block.  
Tools: Semgrep, SonarQube, Snyk Code  

###  SCA (Automatic, Static)
It will look into your requirements.txt and give you the known issues in your third party dependencies, along with the installed and fixed version (if fix is available)
Tools: Trivy, OWASP Dependency-Check, Snyk Open Source  

### DAST (Automatic, Dynamic)
It will run set of automated malicious inputs on your running application
Tools: OWASP ZAP, Burp Suite,

### Penetration Testing (Manual, Dynamic)
Tester manually tries to break the security of the system.

