import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BillsTable } from './bills-table';

describe('BillsTable', () => {
  let component: BillsTable;
  let fixture: ComponentFixture<BillsTable>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [BillsTable]
    })
    .compileComponents();

    fixture = TestBed.createComponent(BillsTable);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
