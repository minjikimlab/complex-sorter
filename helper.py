def process_multiple_regions(regions, operations):
    """
    Processes regions and operations to classify them into "Yes" and "No" chromosome tuples.

    Parameters:
    regions (str): Regions in the format [chr_id]:[left]-[right];[chr_id]:[left]-[right];...
    operations (str): Operations in the format [Yes];[No];... where "Yes" means the region
                      should be treated as an AND operation.

    Returns:
    tuple: A tuple containing two lists:
        - List of "Yes" chromosome tuples of the format (chr_id, left, right)
        - List of "No" chromosome tuples of the format (chr_id, left, right)
    """

    # Split the input strings into lists
    region_list = regions.split(';')
    operation_list = operations.split(';')

    yes_chromosomes = []
    no_chromosomes = []

    # Iterate over the regions and corresponding operations
    for region, operation in zip(region_list, operation_list):
        # Parse the region into components
        chr_id, pos = region.split(':')
        left, right = map(int, pos.split('-'))

        # Create the chromosome tuple
        chromosome_tuple = (chr_id, left, right)

        # Append to the respective list based on the operation
        if operation == 'Yes' or operation == 'yes' \
        or operation == 'Y' or operation == 'y':
            yes_chromosomes.append(chromosome_tuple)
        else:
            no_chromosomes.append(chromosome_tuple)

    return yes_chromosomes, no_chromosomes


def process_graphs_arg(arg):
    graphs_flags = {
        "AtoB": False,
        "AtoC": False,
        "BtoA": False,
        "BtoC": False,
        "CtoA": False,
        "CtoB": False,
        "AandC": False,
        "Bcentered": False,
    }

    commands = arg.split(";")
    for command in commands:
        graphs_flags[command] = True
    return graphs_flags


def create_plot_filename(dataset, id, command, numfrag_min, numfrag_max, num_gems):
    """Generate the filename for the plot png image."""
    return f"{dataset}_{id}_{command}_{numfrag_min}_{numfrag_max}_{num_gems}.png"


def create_csv_filename(dataset, path2):
    """Generate the filename for the csv file."""
    return f"{dataset}_{path2}_comp_records.csv"


def create_histogram_filename(dataset, path2):
    """Generate the filename for the histogram text file."""
    return f"{dataset}_{path2}_histogram.txt"


def process_color_arg(colors):
    colors_flags = {
        "anchors": None,
        "fragments": None,
        "lines": None,
    }

    colors = colors.split(';')
    colors_flags["anchors"] = colors[0]
    colors_flags["fragments"] = colors[1]
    colors_flags["lines"] = colors[2]

    return colors_flags


def figsize_height_scaler(x):
    k = 23 / 47
    b = 189 / 47 + 2
    # calculate y using the equation y = kx + b
    y = k * x + b
    return y


def kb_format(x, pos):
    """Convert x-axis tick labels to kb, formatted with commas."""

    kb_value = x / 1000
    if kb_value.is_integer():
        return f'{int(kb_value):,} kb'
    else:
        return f'{kb_value:,.1f} kb'


def create_plot_title(id, input_filename, command, anchors):
    l = anchors[0].split('\t')
    anchor_a = f"{l[0]}:{l[1]}-{l[2]}"

    m = anchors[1].split('\t')
    anchor_b = f"{m[0]}:{m[1]}-{m[2]}"

    r = anchors[2].split('\t')
    anchor_c = f"{r[0]}:{r[1]}-{r[2]}"

    return f"{id}\n{input_filename}\nA: {anchor_a}; B: {anchor_b}; C: {anchor_c}\n{command}"


def generate_filter_regions(input_bedfile, output_bedfile):
    with open(input_bedfile, 'r') as infile, open(output_bedfile, 'w') as outfile:
        for line in infile:
            anchors = line.strip().split('\t')
            filter_region = f"{anchors[0]}\t{anchors[1]}\t{anchors[8]}"
            outfile.write(f"{filter_region}\t{line}\n")
