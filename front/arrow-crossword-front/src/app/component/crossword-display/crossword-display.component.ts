import { Component } from '@angular/core';
import { Capelito } from '../../model/capelito.model';
import { Game } from '../../model/game.model';
import { Cell } from '../../model/cell.model';
import { CommonModule } from '@angular/common';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatButtonModule } from '@angular/material/button';
import { MatInputModule } from '@angular/material/input';
import { MatIconModule } from '@angular/material/icon';

@Component({
  selector: 'app-crossword-display',
  standalone: true,
  imports: [
    CommonModule,
    MatInputModule,
    MatButtonModule,
    MatTooltipModule,
    MatIconModule,
  ],
  templateUrl: './crossword-display.component.html',
  styleUrl: './crossword-display.component.scss',
})
export class CrosswordDisplayComponent {
  game: Game = {
    map_file: 'path/to/map',
    date: '2024-08-29',
    capelitos: [
      {
        capelito_type: 'horizontal',
        i: 1,
        j: 1,
        word: 'HELLO',
        definition: 'A greeting',
        is_custom_capelito: true,
        direction: 'DOWN',
      },
      {
        capelito_type: 'vertical',
        i: 3,
        j: 3,
        word: 'WORLD',
        definition: 'The Earth',
        is_custom_capelito: false,
        direction: 'DOWN',
      },
    ],
    mystery_capelito: {
      word: 'MYSTERY',
      word_letters: [
        ['M', 0, 2],
        ['Y', 1, 2],
        ['S', 2, 2],
        ['T', 3, 2],
        ['E', 4, 2],
        ['R', 5, 2],
        ['Y', 6, 2],
      ],
      definition: 'Something not understood',
    },
  };

  userEntries: Cell[][] = Array.from({ length: 9 }, () =>
    Array.from({ length: 5 }, () => ({
      value: '',
      locked: false,
    }))
  );

  constructor() {}

  ngOnInit(): void {
    this.initializeUserEntries();
  }

  initializeUserEntries(): void {
    this.game.capelitos.forEach((capelito: Capelito) => {
      this.userEntries[capelito.i][capelito.j] = {
        value: capelito.word[0],
        locked: true,
        definition: capelito.definition,
        direction: capelito.direction,
      };
    });
  }

  getLetter(i: number, j: number): string {
    return this.userEntries[i][j].value;
  }

  onUserInput(i: number, j: number, event: any) {
    console.log(
      'i j value',
      i,
      j,
      event.target.value.toUpperCase().slice(0, 1)
    );
    this.userEntries[i][j].value = event.target.value.toUpperCase().slice(0, 1);
  }
}
