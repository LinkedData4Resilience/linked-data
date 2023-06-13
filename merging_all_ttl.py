def merge_ttl_files(file1, file2, file3, merged_file):
    with open(file1, 'r', encoding='utf-8') as f1, open(merged_file, 'w', encoding='utf-8') as merged:
        merged.write(f1.read())

    with open(file2, 'r', encoding='utf-8') as f2, open(merged_file, 'a', encoding='utf-8') as merged:
        next(f2)  # Skip header line (if any)
        merged.write(f2.read())

    with open(file3, 'r', encoding='utf-8') as f3, open(merged_file, 'a', encoding='utf-8') as merged:
        next(f3)  # Skip header line (if any)
        merged.write(f3.read())

# Usage example
file1 = 'converted_EOR-2023-04-30.ttl'
file2 = 'converted_ukr-civharm-2023-04-30.ttl'
file3 = 'Merged-2023-04-30.ttl'
merged_file = 'all_ttl.ttl'

merge_ttl_files(file1, file2, file3, merged_file)
