# This is a script designed to help with updating mailing addresses
# in Little Green Light. The output can be used with the flex importer
# to update LGL records with addresses if they previously did not have
# one. This script requires 2 CSV files as input: One should be address
# information from all constituents in LGL, and the other should contain
# the new addresses associated with people's information.
# Make sure the columns are ordered this way in both files:
# First Name, Last Name, Street, City, State, Zip, and Email

# I wrote this script because Audrey noticed that a lot of participants
# in LGL did not have addresses, and this became a problem when the staff
# had the idea of mailing things to participants. New address information
# was made available through the enrollment Google Forms.

lgl_addresses = open("lgl_addresses.csv", "r")
new_addresses = open("new_addresses.csv", "r")
updated_addresses = open("updated_addresses.csv", "w")

lgl_lines = [line.split(",") for line in lgl_addresses.readlines()]
new_lines = [line.split(",") for line in new_addresses.readlines()]
combined_lines = []
number_of_matches = 0
expected_matches = len(new_lines)
number_of_updates = 0
first_row = new_lines[0]

for new_line in new_lines:
  matched = 0
  first_name = '"' + new_line[0].strip().casefold() + '"'
  last_name = '"' + new_line[1].strip().casefold() + '"'
  pref_email = '"' + new_line[6].strip().casefold() + '"'
  for lgl_line in lgl_lines:
    lgl_first_name = lgl_line[0].strip().casefold()
    lgl_last_name = lgl_line[1].strip().casefold()
    lgl_pref_email = lgl_line[6].strip().casefold()
    if lgl_first_name == first_name and lgl_last_name == last_name and lgl_pref_email == pref_email:
      print("MATCH FOR", lgl_first_name, lgl_last_name)
      number_of_matches += 1
      matched = 1
      output_line = new_line

      # It's great if there is a match, but the issue now is what
      # to do in two cases:
      # 1) The lgl record does NOT have an address at all
      # 2) Both the lgl record and the Audrey record have addresses
      # The second case also includes situations where lgl records are
      # partially incomplete (street address but no state or zip)

      # To solve case 1, I can assume that the Audrey addresses all have a 
      # Street address, and that if there is no street address in lgl,
      # the data is USELESS anyway, so we want to put in the Audrey address

      lgl_street = lgl_line[2]
      if lgl_street == '""':
        updated_addresses_lines.append(output_line)

      # Now, what happens if the lgl Street is NOT empty?
      else:
        number_of_updates += 1
        # First of all, replace the Audrey Street with the lgl street
        output_line[2] = lgl_street
        # Then, use three more IF statements to check the city, state, and ZIP
        lgl_city = lgl_line[3]
        lgl_state = lgl_line[4]
        lgl_zip = lgl_line[5]

        if lgl_city == '""':
          pass
        else:
          output_line[3] == lgl_city

        if lgl_state == '""':
          pass
        else:
          output_line[4] == lgl_state

        if lgl_zip == '""':
          pass
        else:
          output_line[5] = lgl_zip

        # Finally, append the output line!
        updated_addresses_lines.append(output_line)

    else:
      pass
  if matched == 0:
    print("NO MATCH FOR", first_name, last_name, pref_email)

string_to_write = ",".join(first_row)
updated_addresses.write(string_to_write)

for line in updated_addresses_lines:
  string_to_write = ",".join(line)
  updated_addresses.write(string_to_write)

lgl_addresses.close()
new_addresses.close()
updated_addresses.close()

# There is a discrepancy here because of small errors in either
# file. I will investigate these issues later when we switch
# CRM platforms.
print("NUMBER OF MATCHES:", number_of_matches)
print("EXPECTED MATCHES", expected_matches)
print("NUMBER OF UPDATES", number_of_updates)