import re

MOLECULE_REGEX = '^[a-zA-Z0-9()\\[\\]{}]*$'
CLOSED_BRACKETS = {'(': ')', '[': ']', '{': '}'}


def validate_molecule_format(molecule):
  """
  Validation of the input molecule to avoid null molecule and run some obvious check such as:
  - molecule is not null and is a string.
  - regex check to ensure alphanumeric chars with the three allowed type of brackets.
  - molecule must begin with an atom, so with an upper char.
  More validations could be implement to check open brackets are well closed and so one, but it will add up some processing
  time to the parse_molecule() method, so these types of control can be done directly inside the processing method
  parse_molecule().

  :param molecule : input molecule to validate before parsing it.
  """
  if not molecule:
    raise Exception('Molecule must be not null.')
  elif not isinstance(molecule, str):
    raise Exception(f'Molecule must be a string. Check type of input molecule {molecule}')
  elif len(molecule) == 0 or not re.match('[A-Z]', molecule[0]) or not re.fullmatch(MOLECULE_REGEX, molecule):
    raise Exception(f'Invalid input molecule format for {molecule}.')
  else:
    return molecule


def get_index(index: str):
  return int(index) if index else 1


def update_parsed_molecule(parsed_molecule: dict, embedded_parse_molecule: dict, index_wrapper: int):
  """
  Updating parent parsed molecule values with the embedded parsed molecule using the index wrapping the embedded molecule
  with brackets.
  """
  for atoms in embedded_parse_molecule:
    if atoms in parsed_molecule:
      parsed_molecule[atoms] = parsed_molecule[atoms] + embedded_parse_molecule[atoms] * index_wrapper
    else:
      parsed_molecule[atoms] = embedded_parse_molecule[atoms] * index_wrapper
  return parsed_molecule


def parse_molecule(molecule_to_parse):
  """
  Parsing molecule through a while loop to compute atoms assuming :
  - atoms are on one upper char or one upper char and one lower case.
  - stoichiometric coefficient are integers.
  Embedded molecules found inside opened and closed brackets are computed through recursion.

  :param molecule_to_parse: input molecule that will be first validate and then compute.
  :return: dict containing the parse molecule with atoms as key and total number of atoms in the current molecule
   as value
  :raise : exception will be raised for incorrect used of brackets.
  """
  molecule = validate_molecule_format(molecule_to_parse)
  parsed_molecule = {}
  index = None
  atoms = None
  embedded_molecule = ''
  end_bracket = None
  i = 0
  while i < len(molecule):
    if not end_bracket:
      if molecule[i].isalpha() and molecule[i].isupper():
        if atoms:
          parsed_molecule[atoms] = get_index(index)
          index = None
        atoms = molecule[i]
      elif molecule[i].isalpha() and molecule[i].islower():
        atoms += molecule[i]
      elif molecule[i].isnumeric():
        index = molecule[i] if not index else index + molecule[i]
      elif re.match("[({\\[]", molecule[i]):
        end_bracket = CLOSED_BRACKETS[molecule[i]]
        if atoms:
          parsed_molecule[atoms] = get_index(index)
          atoms = None
          index = None
      elif re.match('[)}\\]]', molecule[i]):
        raise Exception(f'Invalid molecule format : bracket {molecule[i]} is closed but never opened.')

    else:
      if molecule[i] == end_bracket:
        end_bracket = None
      else:
        embedded_molecule += molecule[i]
    i += 1
  if atoms:
    parsed_molecule[atoms] = get_index(index)
    index = None
  if embedded_molecule:
    update_parsed_molecule(parsed_molecule, parse_molecule(embedded_molecule), int(index) if index else 1)
  if end_bracket:
    raise Exception(f'Invalid molecule format : at least one open bracket was not well closed with {end_bracket}')
  return parsed_molecule


if __name__ == '__main__':
  """
  To easily test my code :)
  """
  molecules_ok = ['H2O3', 'Mg4H2O41NFd', 'H2(Mg2N)4', 'Mg(OH{Mg4N[G2F]}3)2']
  for molecule in molecules_ok:
    print(parse_molecule(molecule))
  molecules_ko = [111, None, 'H#ZZZ@_', '2H', 'H2(O2(Mg4', 'H(Mg{)}', 'H2)O']
  for molecule in molecules_ko:
    try:
      print(parse_molecule(molecule))
    except Exception as e:
      print(e)
