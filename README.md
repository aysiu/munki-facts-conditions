# Community Facts for [munki-facts](https://github.com/munki/munki-facts) Use

## Shard
  * Sets a shard value for the hardware based on downloaded Munki catalogs and the hardware serial number.
  * If /Library/Managed Installs/catalogs/development exists when this is run, the shard value will always be set to 0.
  * If /Library/Managed Installs/catalogs/testing exists when this is run, the shard value will be between 1 and 10.
  * If /Library/Managed Installs/catalogs/execs exists when this is run, the shard value will always be 99.
  * If none of those catalogs exists, the shard will be something between 11 and 98, inclusive.
 
 Catalog names and thresholds can be adjusted via dictionary/variable.
