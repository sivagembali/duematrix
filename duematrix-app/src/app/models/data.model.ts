export interface ColumnHeader {
  col_header: string;
  col_label: string;
  is_editable: boolean;
  is_multi_select?: boolean;
  col_width?: number;
  display: boolean;
  display_order: number;
}

export interface DataRow {
  id: number;
  [key: string]: any;
}
