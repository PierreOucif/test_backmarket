import re

MOLECULE_REGEX = '^[a-zA-Z0-9()\\[\\]{}]*$'
CLOSED_BRACKETS = {'(': ')', '[': ']', '{': '}'}


def validate_molecule_format(molecule):
  if len(molecule) == 1 and not re.match('[A-Z]', molecule) or not re.fullmatch(MOLECULE_REGEX, molecule):
    raise Exception(f'Invalid input molecule format for {molecule}')
  else:
    return molecule


def update_parsed_molecule(parse_molecule: dict, embedded_parse_molecule: dict, index_wrapper: int):
  for atoms in embedded_parse_molecule:
    if atoms in parse_molecule:
      parse_molecule[atoms] = parse_molecule[atoms] + embedded_parse_molecule[atoms] * index_wrapper
    else:
      parse_molecule[atoms] = embedded_parse_molecule[atoms] * index_wrapper
  return parse_molecule


def parse_molecule(molecule):
  molecule = validate_molecule_format(molecule)
  parsed_molecule = {}
  index = None
  atoms = None
  n = 0
  for i in range(0, len(molecule)):
    if molecule[i].isalpha() and molecule[i].isupper():
      for j in range(i + 1, len(molecule)):
        if molecule[j].isalpha():
          if molecule[j].isupper():
            parsed_molecule[molecule[i] if not atoms else atoms] = 1 if not index else int(index)
            index = None
            atoms = molecule[j]
            break
          else:
            atoms = molecule[i] + molecule[j]
        elif molecule[j].isnumeric():
          if index:
            index += molecule[j]
          else:
            index = molecule[j]
      i += 1
    elif re.match("[({\\[]", molecule[i]):
      embedded_molecule = None
      end_bracket = CLOSED_BRACKETS[molecule[i]]
      embedded_molecule_is_closed = False
      for j in range(i + 1, len(molecule)):
        if molecule[j] == end_bracket:
          embedded_molecule_is_closed = True
        else:
          if embedded_molecule_is_closed:
            parsed_molecule = update_parsed_molecule(parsed_molecule, parse_molecule(embedded_molecule),
                                                     1 if not molecule[j].isnumeric() else int(molecule[j]))
          else:
            embedded_molecule = molecule[j] if not embedded_molecule else embedded_molecule + molecule[j]
      i += 1
  if atoms:
    parsed_molecule[atoms] = 1 if not index else int(index)
  return parsed_molecule


if __name__ == '__main__':
  for molecule in ['H2O3', 'Mg4H2O41NFd', 'H2(Mg2N)4', 'Mg(OH{Mg4N[G2F]}3)2']:
    print(parse_molecule(molecule))
