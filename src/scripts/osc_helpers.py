def handle_outgoing(address, value):
    out = op('osc_out')  # get the outgoing OSC table operator
    out.clear()                          # wipe previous table rows
    out.appendRow([address, value])      # write a new row
    out.send()                           # commit/send over network
