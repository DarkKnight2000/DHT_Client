#   The Client side application for Distributed File system

##  Installing necessary packages

```
pip3 install Click==7.0 requests==2.23.0 cryptography==2.6.1
```

## Running the CLI

* To upload a file:

    ```
    python3 filestore.py upload --filename <path_to_file_to_upload> --keysfilename <path_to_store_the_keys>
    ```

* To retrieve a file

    ```
    python3 filestore.py retrieve --filename <path_to_store_retrieved_file> --keysfilename <path_to_keysFile>
    ```