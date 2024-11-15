import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DialogConsultarCodigoComponent } from './dialog-consultar-codigo.component';

describe('DialogConsultarCodigoComponent', () => {
  let component: DialogConsultarCodigoComponent;
  let fixture: ComponentFixture<DialogConsultarCodigoComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [DialogConsultarCodigoComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DialogConsultarCodigoComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
