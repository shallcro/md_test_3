# TEST Style Guide

**Completeness:** Regardless of whether a metadata element is technically required, curators should strive to include information for as many elements as possible. While metadata is often lifted from PI-provided materials, this is not a requirement for metadata. Especially for fields such as “Description of Variables” or “Purpose of the Study” where the curators knowledge of the study should be sufficient to complete the field without PI provided text, curators should draft metadata text when possible.

How to correctly refer to ICPSR studies within metadata text: When using an identifier (study number) within metadata text, “ICPSR” should precede the number, ie. “This collection continues the work of ICPSR 23421.” In these scenarios, the DOI should always be linked as well. DOI links should typically use the unversioned instance of the DOI (ie. doi.org/10.3886/ICPSR37464, as opposed to doi.org/10.3886/ICPSR37464.v1), unless the version is important. For example, if the goal is to direct users to the data, the unversioned DOI is more likely to be appropriate. If there is something specific in the other study’s metadata that is being pointed to, it may make sense to use a versioned DOI in case that metadata changes in a future version.

Four digit numbers do not require a leading 0 when they are referenced with study metadata, but please note that DOIs DO contain leading 0s.

Using a version number within metadata text is somewhat rare, but you can simply append it to the study number, ie. ICPSR 23421-v2.

Using a DOI within metadata text: All DOIs have both “versioned” formats and “unversioned” or V0 formats. Unless there is something in the metadata for a specific version of a study that the metadata is referring to, unversioned DOIs are preferred. Ie. “https://doi.org/10.3886/ICPSR06425” is preferred over “https://doi.org/10.3886/ICPSR06425.v1”. The V0 DOI will always point to the latest version of a study.

**Links:** In general, URLs should not be in the metadata. Rather, when linking, the link should have descriptive text, ie, “more information is available at the project website”, rather than “more information is available at the project website: www.project.edu/project”. This is friendlier to screen readers and web scrapers. A specific exception to this rule is links that are contained in formal citations. This rule applies to all types of URLs, including DOIs. For ICPSR DOIs, the study number can be used as the descriptive text.

**Versioning:** Any update with a change to the version number must come with a corresponding addition to the “Changes to the Collection” field.

The standard ICPSR Version Statement consists of the designation ICPSR (uppercase) plus the full 5-digit study number (including any leading zeros), a dash followed by a lowercase "v", and the version number.

The Version field is used as the source of the version identifier for the Citation field. Each version also receives a unique DOI (unversioned DOIs redirect to the current version). 

**VIAF and Authority Control:** The authority for organizational names is the Virtual International Authority File, or [VIAF](https://viaf.org/). VIAF is an effort to link the various national authority files (that is, catalogs of authoritative names such as the Library of Congress Name Authority File) into a single international collective. PI Affiliations should be searched in VIAF. Once the record for the entity is found, those inputting metadata should click on the link next to the American flag (which will lead to the Library of Congress entry), and use the name in the 110 field of the MARC record displayed. If there are only foreign catalog entries, use of those are acceptable. 

If a PI affiliation does not have a VIAF record, the ICPSR’s internal organizational thesaurus should be checked. If there is not an existing entry in the ICPSR’s internal thesaurus, the PI’s provided affiliation name is acceptable.

**Tense:** Use past tense when describing the process of collecting the data.  Use present tense when necessary, such as when you are describing the data: “The MIDUS Refresher collection is split into two datasets.”

Numbers: Always use numerals versus spelling numbers out. Spelling out the number can sometimes be used for emphasis, but in that case, the number should also be used in parenthesis (e.g. Two thousand (2,000)).

**Example of Sampling vs. Universe:**
- **Sampling:** The data collection is a pooled cross-sectional time-series of bank robberies in 50 states over a period of 6 years (1970-1975), resulting in 300 observations.  Universe: Bank robberies in the 50 states.
- **Sampling:** Three target groups were identified: lawyers 36 years of age and above who were members of the American Bar Association (ABA), all the remaining members of the ABA excluding law students, and all lawyers in the nonmember files kept by the ABA. A systematic random probability sample was drawn to represent each of the three groups. The group of young lawyers was oversampled. Universe: Lawyers in the United States in 1984. 