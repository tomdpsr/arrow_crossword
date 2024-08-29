import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CrosswordDisplayComponent } from './crossword-display.component';

describe('CrosswordDisplayComponent', () => {
  let component: CrosswordDisplayComponent;
  let fixture: ComponentFixture<CrosswordDisplayComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CrosswordDisplayComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CrosswordDisplayComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
