export type ProductivitySnapshot = {
  notes: boolean;
  tasks: boolean;
  calendarUi: false;
  mailClient: false;
  editor: false;
  source: 'studio';
};

export function buildProductivity(): ProductivitySnapshot {
  return {
    notes: true,
    tasks: true,
    calendarUi: false,
    mailClient: false,
    editor: false,
    source: 'studio',
  };
}
