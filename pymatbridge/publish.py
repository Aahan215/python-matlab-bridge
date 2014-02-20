import IPython.nbformat.current as nbformat
import numpy as np

def format_line(line):
    """
    Format a line of Matlab into either a markdown line or a code line.

    Parameters
    ----------
    line : str
        The line of code to be formatted. Formatting occurs according to the
        following rules:

        - If the line starts with (at least) two %% signs, a new cell will be
          started.

        - If the line doesn't start with a '%' sign, it is assumed to be legit
          matlab code. We will continue to add to the same cell until reaching
          the next comment line
    """
    if line.startswith('%%'):
        md = True
        new_cell = True
        source = line.split('%%')[1]

    elif line.startswith('%'):
        md = True
        new_cell = False
        source = line.split('%')[1]

    elif line == '\n':
        md = False
        new_cell = True
        source = ""
    else:
        md = False
        new_cell = False
        source = line

    return new_cell, md, source

def mfile_to_lines(mfile):
    """
    Read the lines from an mfile

    Parameters
    ----------
    mfile : string
        Full path to an m file
    """
    # We should only be able to read this file:
    f = file(mfile, 'r')
    lines = f.readlines()
    f.close()
    return lines

def lines_to_notebook(lines, name=None):
    """

    """
    source = []
    md = np.empty(len(lines), dtype=object)
    new_cell = np.empty(len(lines), dtype=object)
    for idx, l in enumerate(lines):
        new_cell[idx], md[idx], this_source = format_line(l)
        source.append(this_source)
    # This defines the breaking points between cells:
    new_cell_idx = np.hstack([np.where(new_cell)[0], -1])

    # Listify the sources:
    cell_source = [source[new_cell_idx[i]:new_cell_idx[i+1]]
                   for i in range(len(new_cell_idx)-1)][0]
    cells = []
    for cell_idx, cell_s in enumerate(cell_source):
        if md[cell_idx]:
            cells.append(nbformat.new_text_cell('markdown', cell_s))
        else:
            cells.append(nbformat.new_code_cell(cell_s, language='matlab'))

    ws = nbformat.new_worksheet(cells=cells)
    notebook = nbformat.new_notebook(metadata=nbformat.new_metadata(),
                                 worksheets=[ws])
    return notebook

def convert_mfile(mfile, outfile=None):
    """
    Convert a Matlab m-file into a Matlab notebook in ipynb format

    Parameters
    ----------
    mfile : string
        Full path to a matlab m file to convert

    outfile : string (optional)
        Full path to the output ipynb file

    """
    if outfile is None:
        outfile = fname.split('.m')[0] + '.ipynb'
    nbfile = file(outfile, 'w')
    nbformat.write(notebook, nbfile, format='ipynb')
    nbfile.close()
