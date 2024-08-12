current_lgl_addresses = open("current_lgl_addresses.csv", "r")
audrey_addresses = open("audrey_addresses.csv", "r")
addresses_without_duplicates = open("addresses_without_duplicates.csv", "w")

lgl_lines = [line.split(",") for line in current_lgl_addresses.readlines()]
audrey_lines = [line.split(",") for line in audrey_addresses.readlines()]
addresses_without_duplicates_lines = []
number_of_matches = 0
expected_matches = len(audrey_lines)

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
    else:
      pass
  if matched == 0:
    print("NO MATCH FOR", first_name, last_name, pref_email)
      
current_lgl_addresses.close()
audrey_addresses.close()
addresses_without_duplicates.close()

print("NUMBER OF MATCHES:", number_of_matches)
print("EXPECTED MATCHES", expected_matches)