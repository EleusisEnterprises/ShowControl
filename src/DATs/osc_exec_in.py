# me - this DAT.
# 
# dat - the changed DAT
# rows - a list of row indices
# cols - a list of column indices
# cells - the list of cells that have changed content
# prev - the list of previous string contents of the changed cells
# 
# Make sure the corresponding toggle is enabled in the DAT Execute DAT.
# 
# If rows or columns are deleted, sizeChange will be called instead of row/col/cellChange.


def onTableChange(dat):
    # Skip header row
    for row in dat.rows()[1:]:
        address = row[0].val       # the OSC address string
        value   = float(row[1].val) # the numeric value
        import osc_helpers       # your external Python module
        osc_helpers.handle_incoming(address, value)
    return


def onRowChange(dat, rows):
	return

def onColChange(dat, cols):
	return

def onCellChange(dat, cells, prev):
	return

def onSizeChange(dat):
	return
	