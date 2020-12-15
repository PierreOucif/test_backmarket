import re

MOLECULE_REGEX = '^[a-zA-Z0-9()\\[\\]{}]*$'
CLOSED_BRACKETS = {'(': ')', '[': ']', '{': '}'}


def validate_molecule_format(molecule):
  if len(molecule) == 1 and not re.match('[A-Z]', molecule) or not re.fullmatch(MOLECULE_REGEX, molecule):
    raise Exception(f'Invalid input molecule format for {molecule}')
  else:
    return molecule


def parse_molecule(molecule):
  molecule = validate_molecule_format(molecule)
  parsed_molecule = {}
  index = None
  atoms = None
  for i in range(0, len(molecule)):
    if molecule[i].isalpha() and molecule[i].isupper():
      for j in range(i + 1, len(molecule)):
        if molecule[j].isalpha():
          if molecule[j].isupper():
            parsed_molecule[molecule[i] if not atoms else atoms] = 1 if not index else index
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
  if atoms:
    parsed_molecule[atoms] = 1 if not index else index
  return parsed_molecule


if __name__ == '__main__':
  for molecule in [ 'H2O3', 'Mg4H2O41NFd','Mg(OH)2']:
    print(parse_molecule(molecule))
