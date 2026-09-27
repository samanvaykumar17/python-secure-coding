# Secure Coding Landscape   

## Types of Testing
We can do four types of automated vulnerability testing  

### SAST (Automatic, Static Application Code)  
Static Application Security Testing  
It will look into your source code repository and find issues.  It will even give you the filename and line number of the problematic code block.  
Tools: Semgrep, SonarQube, Snyk Code  

###  SCA (Automatic, Static Dependency Code)
Software Composition Analysis   
It will look into your requirements.txt and give you the known issues in your third party dependencies, along with the installed and fixed version (if fix is available)  
Tools: Trivy, OWASP Dependency-Check, Snyk Open Source  

### DAST (Automatic, Dynamic)
Dynamic Application Security Testing  
It will run set of automated malicious inputs on your running application  
Tools: Burp Suite, OWASP ZAP  

### Penetration Testing (Manual, Dynamic)   
Tester manually tries to break the security of the system.

## Cataloguing of vulnerabilities

There are two types of standardized cataloging:

### CWE (Common Weakness Enumeration)
These are conceptual weaknesses which can occur in any (web) application in any language or library, be it your source code or a dependency.   
For Example:  
CWE-89 (SQL Injection)   
CWE-79 (Cross Site Scripting)  

As of September 2025, there are about 1500 CWEs. Their number grows relatively slower than CVE, as they are concepts.  

### CVE (Common Vulnerabilities and Exposures)
These are particular vulnerabilities in specific version of a specific package of a specific language.  
For Example:  
CVE-2026-4519: webbrowser.open() built-in module function of python allows URLs beginning with "-" which can lead to Command injection (CWE-78)  


CVE-2026-3087: shutil.unpack_archive()  built-in module function of python in windows can extract a zip outside target directory which can lead to Path Traversal (CWE-22)  

As of September 2025, there are about 70,000 CVEs. Their number is quickly growing by 10,000-20,000 new CVEs every year.  

#### Infamous Recent CVEs
CVE-2021-44228: Log4Shell  
CVE-2026-42208: LiteLLM  

### Relationship between CVE and CWE
CVEs can be mapped to CWEs.  
CVE is the symptom.  
CWE is the root cause.  


## Governance
CVEs are cataloged in CVE program of US Govt managed by MITRE. NVD (National Vulnerabillity Database) provides additional information on these CVEs.
CWEs are cataloged by MITRE Corporation.  

In 2025, the Trump administration briefly planned on defunding the CVE program and security experts said that the results of this defunding can be catastrophic as the whole world depends on CVE and CWEs for vulnerabilties.  

## Top Lists
OWASP Top 10 releases a list of 10 most dangerous families of vulnerabilities once every 3-4 years. Each of the top 10 families may contain 4-5 CWEs.  
MITRE Top 25 releases a list of 25 most dangerous CWEs of vulnerabilities every year.  

# False Positives
Sometimes the vulnerabilities reported by SAST/SCA tools will not be exploitable in our case  4

## Reachability
For example: you are using a math library whose graphs module has a CVE. But you are just using the stats module.  

## Platform
For example: the CVE is application only to windows environments, but you are using linux.  

## Firewall/Infrastructure

For example: You have a regular expression ReDoS vulnerability but you firewall allows only 100 requests in 1 minute. Or you have a library allows outbound requests to vulnerable endpoint, but your VPN settings restricts the hosts to which outbound call can be made.   

# Remediation

After analysing whether the vulnerability is a true positive for your case, you need to remediate it.  

## SAST  
In case of SAST, you need to make changes to your source code by following the CWE-specific secure coding practices to replace the vulnerable code. Your code changes should not break the code or contract with downstream applications and thus appropriate tests are needed.    

## SCA 
In case of SCA, you need to upgrade the vulnerable library to the available patch, after analyzing how it will affect your code. Whether the migration will break your existing code, will the package upgrade introduce new and even more dangerous vulnerabilities, or if you need to find a suitable alternative to the given library. The same package may be used in multiple other microservices, which may contain the same vulnerability. Thus you may reuse the same strategy to remediate the same CVE in other repositories. If changing the packge version is not possible you may need to apply compensating controls (in code or infrastructure) to make sure that the vulnerabilities are not exploitable.  
