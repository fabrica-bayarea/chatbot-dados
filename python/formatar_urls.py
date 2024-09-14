def format_urls(input_file, output_file):
    with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
        f_out.writelines(f'"{url.strip()}",\n' for url in f_in)

input_file = 'links.txt'
output_file = 'links_formatados.txt'

format_urls(input_file, output_file)