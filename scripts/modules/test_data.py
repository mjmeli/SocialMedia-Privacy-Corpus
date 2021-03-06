"""
    test_data.py
    Responsible for all test data related stuff
"""
import os
import sys
from . import api, data, helpers

# Write out a test data record to string
def get_test_data_record(articleId, title, lead, content, tags):
    record = {
        'id': articleId,
        'class': None,
        'title': title,
        'lead': lead,
        'content': content,
        'tags': tags,
        'core-words': None,
        'words': None
    }
    record_json = helpers.json_object_to_string(record)
    return record_json

# Retrieve the content for each ID and write it out to file
def get_test_data_files_for_ids(ids, hashes, folder, shouldReuse=True, progress=False):
    # Statistics
    numRetrieved = 0
    numCached = 0
    for index, (i, h) in enumerate(zip(ids, hashes)):
        # Print out progress is flag set
        if progress:
            sys.stdout.write("\r{}/{}".format(index + 1, len(ids)))
            sys.stdout.flush()
        # Only retrieve and write out if the file does not exist already
        # (save API calls) unless told otherwise
        filepath = os.path.join(folder, h)
        if not os.path.exists(filepath) or not shouldReuse:
            title, lead, content, tags = api.get_title_lead_body_tags_for_article_id(i)
            record_json = get_test_data_record(i, title, lead, content, tags)
            data.write_string_to_file(filepath, record_json)
            numRetrieved = numRetrieved + 1
        else:
            numCached = numCached + 1
    if progress:
        sys.stdout.write("\n")
        sys.stdout.flush()
    return (numRetrieved, numCached)
