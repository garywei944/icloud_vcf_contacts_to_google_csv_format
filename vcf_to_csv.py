import pandas as pd
import re

import logging
import sys

logging.basicConfig(level=logging.WARNING, stream=sys.stderr)


def format_phone(_phone):
    """
    Format the phone number to the format like +86 123 4567 8900, +1 123 456 7890, or 010 1234 5678
    Only handles prefix that are +86, +1, or 010
    :param _phone: phone number, allow characters other than numbers
    :return: formatted phone number
    """
    pre = ''
    if _phone[:3] == '+86':
        _phone = _phone[3:]
        pre = '+86 '
    elif _phone[:2] == '+1':
        _phone = _phone[2:]
        pre = '+1 '

    _phone = re.sub('[^0-9]', '', _phone)
    if _phone[:3] == '010':
        pre += '010 '
        _phone = _phone[3:]
    if len(_phone) == 8:
        _phone = "{} {}".format(_phone[:4], _phone[-4:])
    elif len(_phone) == 10 or len(_phone) == 11:
        _phone = "{} {} {}".format(_phone[:3], _phone[3:-4], _phone[-4:])
    # logging.debug(pre+_phone)
    return pre + _phone


def insert_phone(result, _i, _type, _value):
    """
    Insert phone number to a certain row
    :param result: the DataFrame of converted contacts
    :param _i: index of the current contact
    :param _type: 'Home', 'Work', 'Other', etc
    :param _value: phone number
    :return: None
    """
    for j in range(1, 6):
        if pd.isna(result.loc[_i, 'Phone {} - Value'.format(j)]):
            result.loc[_i, 'Phone {} - Type'.format(j)] = _type
            result.loc[_i, 'Phone {} - Value'.format(j)] = _value
            return

    logging.warning("Some phone number lost! {}".format(result.loc[_i, 'Name']))
    logging.debug(result.iloc[_i, :])


def insert_email(result, _i, _type, _value):
    """
    Insert E-mail address to a certain row
    :param result: the DataFrame of converted contacts
    :param _i: index of the current contact
    :param _type: 'Home', 'Work', 'Other', etc
    :param _value: E-mail address
    :return: None
    """
    for j in range(1, 3):
        if pd.isna(result.loc[_i, 'E-mail {} - Value'.format(j)]):
            result.loc[_i, 'E-mail {} - Type'.format(j)] = _type
            result.loc[_i, 'E-mail {} - Value'.format(j)] = _value
            return

    logging.warning("Some Email lost! {}".format(result.loc[_i, 'Name']))
    logging.debug(result.iloc[_i, :])


def vcf_to_csv(path='contacts.vcf'):
    """
    Convert the iCloud .vcf contacts to Google .csv format and save into 'converted_contacts.csv'
    Only preserve names, phonetic of names, phone numbers, emails, birthday, company, title, and notes
    Address and other information are not preserved.
    :param path: the path of file that to be processed, iCloud .vcf file in vcard 3.0 format
    :return: pd.DataFrame of the converted csv file
    """
    with open(path, 'r') as file:
        data = file.read().split('BEGIN:VCARD\nVERSION:3.0\n')[1:]

    csv_example = pd.read_csv('contacts.csv')
    result = pd.DataFrame(columns=csv_example.columns, index=range(len(data)))

    for i, record in enumerate(data):
        lines = record.split('\n')[:-2]
        for attributes in lines:
            entries = re.split('[;:]', attributes.replace(u'\xa0', ' '))
            key = entries[0]
            # logging.debug(entries)
            if key == 'N':
                if entries[1] != '':
                    result.loc[i, 'Family Name'] = entries[1]
                if entries[2] != '':
                    result.loc[i, 'Given Name'] = entries[2]
                if entries[3] != '':
                    result.loc[i, 'Additional Name'] = entries[3]
                    # result.loc[i, 'Nickname'] = entries[3]
            elif key == 'FN':
                result.loc[i, 'Name'] = entries[1]
            elif key == 'X-PHONETIC-FIRST-NAME':
                result.loc[i, 'Given Name Yomi'] = entries[1]
            elif key == 'X-PHONETIC-LAST-NAME':
                result.loc[i, 'Family Name Yomi'] = entries[1]
            elif key == 'NICKNAME':
                result.loc[i, 'Nickname'] = entries[1]
            elif 'TEL' in key:
                phone = format_phone(entries[-1])
                if 'type=WORK' in entries:
                    _type = 'Work'
                elif 'type=HOME' in entries:
                    _type = 'Home'
                else:
                    _type = 'Other'
                insert_phone(result, i, _type, phone)
            elif key == 'BDAY':
                result.loc[i, 'Birthday'] = entries[-1].replace('1604', '-')
            elif key == 'ORG':
                result.loc[i, 'Organization 1 - Name'] = entries[1]
                pass
            elif key == 'TITLE':
                result.loc[i, 'Organization 1 - Title'] = entries[1]
                pass
            elif key == 'NOTE':
                result.loc[i, 'Notes'] = entries[-1]
            elif 'EMAIL' in key:
                email = entries[-1]
                if 'type=WORK' in entries:
                    _type = 'Work'
                elif 'type=HOME' in entries:
                    _type = 'Home'
                else:
                    _type = 'Other'
                insert_email(result, i, _type, email)
                pass
            elif 'ADR' in key:
                pass
            elif key == 'REV':
                pass
            elif key == 'PRODID':
                pass
            elif key == 'X-SOCIALPROFILE':
                pass
            elif 'Label' in key:
                pass
            elif len(entries) == 1:
                pass
            else:
                # Print entries that are not processed
                logging.debug(entries)
                pass
    result.to_csv('converted_contact.csv', index=False)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        vcf_to_csv(sys.argv[1])
    else:
        vcf_to_csv('contacts.vcf')
