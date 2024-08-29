import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { CrosswordDisplayComponent } from './component/crossword-display/crossword-display.component';
import { WordInputComponent } from './component/word-input/word-input.component';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    CommonModule,
    RouterOutlet,
    WordInputComponent,
    CrosswordDisplayComponent,
  ],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss',
})
export class AppComponent {
  public customWords: string[] = [];
}
