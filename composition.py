import json
import torch

class Composition(object):
    def __init__(self):
        self.initialize = False

    def __getattribute__(self, attribute):
        if object.__getattribute__(self, 'initialize') is None:
            message = 'please call "compositions.init(compositions_file)" first'
            raise Composition.NotInitializeError(message)
        return object.__getattribute__(self, attribute)

    def init(self, file_path):
        with open(file_path, encoding='utf-8') as file:
            self.compositions = json.load(file)
            pass
        
        self.unit_list = set()
        for composition in self.compositions.values():
            self.unit_list |= set(composition)
        self.unit_list = sorted(self.unit_list, key=self.sort_unit)
        self.sequence_length = len(self.unit_list)

        unit_indices = {
            unit: index
            for index, unit in enumerate(self.unit_list)
        }
        self.unit_sequences = {}
        self.unit_counts = {}
        for character, composition in self.compositions.items():
            composition = set(composition)
            unit_sequence = torch.zeros(self.sequence_length)
            for unit in composition:
                index = unit_indices[unit]
                unit_sequence[index] = 1
                count = self.unit_counts.get(unit, 0)
                self.unit_counts[unit] = count + 1
            self.unit_sequences[character] = unit_sequence
        
        self.unit_counts = {
            unit: self.unit_counts[unit]
            for unit in self.unit_list
        }
        self.initialize = True
    
    def get_characters(self):
        return sorted(self.compositions.keys())
    def get_composition(self, character):
        return self.compositions[character]
    def get_unit_sequence(self, character):
        return self.unit_sequences[character]
    def get_unit_by_sequence(self, unit_sequence):
        return [
            self.unit_list[index]
            for index, value in enumerate(unit_sequence)
            if value
        ]
    
    def sort_unit(self, unit):
        try:
            return int(unit)
        except:
            return 1000 + ord(unit[0]) * len(unit)
    
    class NotInitializeError(Exception):
        pass

compositions = Composition()

if __name__ == '__main__':
    compositions_file = './dataset/compositions.json'
    character = '龍'

    compositions.init(compositions_file)

    characters = compositions.get_characters()
    sequence_length = compositions.sequence_length
    ground_truth = compositions.get_composition(character)
    unit_sequence = compositions.get_unit_sequence(character)
    units = compositions.get_unit_by_sequence(unit_sequence)
    counts = compositions.unit_counts.values()

    ground_truth = ', '.join(ground_truth)
    width_3 = max(len('ground truth'), len(ground_truth))
    units = ', '.join(units)
    width_2 = max(len('predict'), len(units))

    print(f'characters  : {len(characters)}')
    print(f'units       : {sequence_length}')
    print(f'unit counts : {min(counts)} ~ {max(counts)}')
    print()
    print(f'character | {"predict":{width_2}} | {"ground truth":{width_3}}')
    print(f'{character:^8} | {units:{width_2}} | {ground_truth:{width_3}}')
