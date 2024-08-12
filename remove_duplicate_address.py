# To use this, get LGL report data, and then match the Audrey addresses
# CSV so the columns are in the same order in both files.
# You only need to get 7 columns: First Name, Last Name,
# Street, City, State, Zip, and Email

current_lgl_addresses = open("current_lgl_addresses.csv", "r")
audrey_addresses = open("audrey_addresses.csv", "r")
addresses_without_duplicates = open("addresses_without_duplicates.csv", "w")

lgl_lines = [line.split(",") for line in current_lgl_addresses.readlines()]
audrey_lines = [line.split(",") for line in audrey_addresses.readlines()]
addresses_without_duplicates_lines = []
number_of_matches = 0
expected_matches = len(audrey_lines)
number_of_updates = 0

for audrey_line in audrey_lines:
  matched = 0
  first_name = '"' + audrey_line[0].strip().casefold() + '"'
  last_name = '"' + audrey_line[1].strip().casefold() + '"'
  pref_email = '"' + audrey_line[6].strip().casefold() + '"'
  for lgl_line in lgl_lines:
    lgl_first_name = lgl_line[0].strip().casefold()
    lgl_last_name = lgl_line[1].strip().casefold()
    lgl_pref_email = lgl_line[6].strip().casefold()
    if lgl_first_name == first_name and lgl_last_name == last_name and lgl_pref_email == pref_email:
      print("MATCH FOR", lgl_first_name, lgl_last_name)
      number_of_matches += 1
      matched = 1
      output_line = audrey_line

      # It's great if there is a match, but the issue now is what
      # to do in two cases:
      # 1) The LGL record does NOT have an address at all
      # 2) Both the LGL record and the Audrey record have addresses
      # The second case also includes situations where LGL records are
      # partially incomplete (street address but no state or zip)

      # To solve case 1, I can assume that the Audrey addresses all have a 
      # Street address, and that if there is no street address in LGL,
      # the data is USELESS anyway, so we want to put in the Audrey address

      lgl_street = lgl_line[2]
      if lgl_street == '""':
        addresses_without_duplicates_lines.append(output_line)

      # Now, what happens if the LGL Street is NOT empty?
      else:
        number_of_updates += 1
        # First of all, replace the Audrey Street with the LGL street
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
        addresses_without_duplicates_lines.append(output_line)

    else:
      pass
  if matched == 0:
    print("NO MATCH FOR", first_name, last_name, pref_email)
      
for line in addresses_without_duplicates_lines:
  string_to_write = ",".join(line)
  addresses_without_duplicates.write(string_to_write)

current_lgl_addresses.close()
audrey_addresses.close()
addresses_without_duplicates.close()

# I can disregard the discrepancy for now, but we want to
# investigate those records later
print("NUMBER OF MATCHES:", number_of_matches)
print("EXPECTED MATCHES", expected_matches)