# label_creator

Aims to generate formatted labels for the Digital Botanical Gardens Intitiative. There are two tools:
- Generate labels from scratch: Requires to have a directus_dbgi username and password and to be at University of Fribourg (or use a VPN). It will generate a user defined number of labels, add them to the directus database and format them in three pdf files (collection labels, extraction labels and injection labels).
- Print already existing labels from a table: Requires a CSV table without header containing already existing codes (already added to the directus_dbgi database) in format dbgi_123456. It will also generate three pdf files (collection labels, extraction labels and injection labels) with the extraction and injection suffixes you want. Be careful: don't use this tool if you want new labels, because it doesn't modify anything in the directus_dbgi database.
- Generate 8x3 labels from scratch: Same as Generate labels from scratch requirements. This perfomrs the same actions, but for falcon racks. Permits to better track the samples in the lab.

For now only available in .exe format (Windows).

For mac or linux users you will need to install python (if not already done), clone the repository, install the related packages and run the code label_creator.py to have the same result.
