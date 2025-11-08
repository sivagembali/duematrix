import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'istDate',
  standalone: true
})
export class IstDatePipe implements PipeTransform {
  transform(value: string | Date | null | undefined, format: string = 'short'): string {
    if (!value) return '';

    const date = new Date(value);
    
    // Convert to IST (UTC+5:30)
    const istDate = new Date(date.toLocaleString('en-US', { timeZone: 'Asia/Kolkata' }));
    
    // Format options based on the format parameter
    const formatOptions: Intl.DateTimeFormatOptions = this.getFormatOptions(format);
    
    return new Intl.DateTimeFormat('en-IN', {
      ...formatOptions,
      timeZone: 'Asia/Kolkata'
    }).format(date);
  }

  private getFormatOptions(format: string): Intl.DateTimeFormatOptions {
    switch (format) {
      case 'short':
        return {
          year: 'numeric',
          month: '2-digit',
          day: '2-digit',
          hour: '2-digit',
          minute: '2-digit',
          hour12: true
        };
      case 'medium':
        return {
          year: 'numeric',
          month: 'short',
          day: 'numeric',
          hour: '2-digit',
          minute: '2-digit',
          hour12: true
        };
      case 'long':
        return {
          year: 'numeric',
          month: 'long',
          day: 'numeric',
          hour: '2-digit',
          minute: '2-digit',
          second: '2-digit',
          hour12: true
        };
      case 'date':
        return {
          year: 'numeric',
          month: '2-digit',
          day: '2-digit'
        };
      case 'time':
        return {
          hour: '2-digit',
          minute: '2-digit',
          hour12: true
        };
      default:
        return {
          year: 'numeric',
          month: '2-digit',
          day: '2-digit',
          hour: '2-digit',
          minute: '2-digit',
          hour12: true
        };
    }
  }
}
