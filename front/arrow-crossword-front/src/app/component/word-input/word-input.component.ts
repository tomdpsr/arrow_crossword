import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Output } from '@angular/core';
import {
  FormArray,
  FormBuilder,
  FormGroup,
  ReactiveFormsModule,
  Validators,
} from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';
import { MatTooltipModule } from '@angular/material/tooltip';

@Component({
  selector: 'app-word-input',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MatInputModule,
    MatButtonModule,
    MatSlideToggleModule,
    MatTooltipModule,
    MatFormFieldModule,
  ],
  templateUrl: './word-input.component.html',
  styleUrl: './word-input.component.scss',
})
export class WordInputComponent {
  wordForm: FormGroup;

  @Output() valider = new EventEmitter<string[]>();

  constructor(private fb: FormBuilder) {
    this.wordForm = this.fb.group({
      words: this.fb.array(
        [],
        [Validators.minLength(1), Validators.maxLength(3)]
      ),
    });

    this.addWord();
  }

  get words() {
    return this.wordForm.get('words') as FormArray;
  }

  addWord() {
    if (this.words.length < 3) {
      this.words.push(this.fb.control('', Validators.required));
    }
  }

  removeWord(index: number) {
    this.words.removeAt(index);
  }

  onSubmit() {
    const wordsArray = this.words.value as string[];
    this.valider.emit(wordsArray);
  }
}
