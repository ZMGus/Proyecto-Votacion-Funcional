import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DialogInscripcionVotanteComponent } from './dialog-inscripcion-votante.component';

describe('DialogInscripcionVotanteComponent', () => {
  let component: DialogInscripcionVotanteComponent;
  let fixture: ComponentFixture<DialogInscripcionVotanteComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [DialogInscripcionVotanteComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DialogInscripcionVotanteComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
