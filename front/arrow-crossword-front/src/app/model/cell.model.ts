import { Direction } from '../type/cell.model';

export interface Cell {
  value: string;
  locked: boolean;
  definition?: string;
  direction?: Direction;
}
