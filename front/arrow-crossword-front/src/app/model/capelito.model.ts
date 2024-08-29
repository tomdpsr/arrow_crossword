import { Direction } from '../type/cell.model';

export interface Capelito {
  capelito_type: string;
  i: number;
  j: number;
  word: string;
  definition: string;
  is_custom_capelito: boolean;
  direction: Direction;
}
