import { Capelito } from './capelito.model';
import { MysteryCapelito } from './mystery-capelito.model';

export interface Game {
  map_file: string;
  date: string;
  capelitos: Capelito[];
  mystery_capelito: MysteryCapelito;
}
