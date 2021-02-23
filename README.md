# iCloud .vcf contacts to Google .csv Format
Convert the iCloud .vcf contacts to Google .csv format and save into 'converted_contacts.csv'

Only preserve names, phonetic of names, phone numbers, emails, birthday, company, title, and notes. Address and other information are not preserved.

## Requirements
* `python3`
* `pandas` - `pip install pandas` or `conda install pandas`

## Usage
```bash
python vcf_to_csv.py <.vcf file>
```
By default, if no commandline argument is provided, the program will try to read and process `contacts.vcf`.

## Features
* Convert iCloud .vcf contacts into Google .csv format.
* Preserve names, phonetic of names, phone numbers, emails, birthday, company, title, and notes.
* Type of phone number and emails like 'Home' and 'Work' are preserved.
* Format phone numbers in the format of +86 123 4567 8900, +1 123 456 7890, or 010 1234 5678. Only support +86, +1, and 010 prefix.
* 5 phone numbers and 2 email addresses supported per contact.

## Files
* `contacts.csv` - Required sample Google .csv format contacts file.
* `contacts.ipynb` - Sandbox codes I used to develop `vcf_to_csv.py`
* `contacts.vcf` - Sample iCloud contacts file, replace it with your own contacts if needed.
* `converted_contact.csv` - Sample output file that is converted from `contacts.vcf`
* `vcf_to_csv.py` - main python implementation, support one commandline argument
