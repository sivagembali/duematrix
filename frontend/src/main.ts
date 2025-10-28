import 'zone.js';
import { bootstrapApplication } from '@angular/platform-browser';
import { AppComponent } from './app/app.component';
import { provideZoneChangeDetection } from '@angular/core';
import { provideHttpClient } from '@angular/common/http';
import { provideAnimations } from '@angular/platform-browser/animations';

// Bootstrap with Zone.js change detection (traditional approach)
bootstrapApplication(AppComponent, {
  providers: [
    provideZoneChangeDetection({ eventCoalescing: true }),
    provideHttpClient(),
    provideAnimations()
  ]
})
  .then(() => {
    console.log('✅ Application started successfully!');
  })
  .catch((err) => {
    console.error('❌ Bootstrap error:', err);
    // Display error to user
    document.body.innerHTML = `
      <div style="padding: 20px; font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; border: 1px solid #ddd; border-radius: 8px;">
        <h1 style="color: #dc3545; margin-bottom: 20px;">
          <i class="fas fa-exclamation-triangle"></i> 
          Application Startup Error
        </h1>
        <div style="background: #f8d7da; color: #721c24; padding: 15px; border-radius: 4px; margin-bottom: 20px;">
          <strong>Error:</strong> Failed to start the Angular application
        </div>
        <h3>Error Details:</h3>
        <pre style="background: #f5f5f5; padding: 15px; border-radius: 4px; overflow: auto; font-size: 12px;">${err.message || err}</pre>
        <div style="margin-top: 20px; padding: 15px; background: #d1ecf1; color: #0c5460; border-radius: 4px;">
          <strong>Next Steps:</strong>
          <ol style="margin: 10px 0 0 20px;">
            <li>Check the browser console for more details</li>
            <li>Verify all dependencies are installed</li>
            <li>Ensure Angular configuration is correct</li>
          </ol>
        </div>
      </div>
    `;
  });
