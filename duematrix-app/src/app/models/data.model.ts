export interface ColumnHeader {
  col_header: string;
  col_label: string;
  is_editable: boolean;
  is_multi_select?: boolean;
  col_width?: number;
  display: boolean;
  default_display: boolean; // Show column by default in the table
  is_frozen: boolean; // Keep column frozen (fixed) on the left
  display_order: number;
}

export interface DataRow {
  id: number;
  [key: string]: any;
}
