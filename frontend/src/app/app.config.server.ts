import { mergeApplicationConfig, ApplicationConfig } from '@angular/core';
import { provideServerRendering } from '@angular/platform-server';
import { provideHttpClient } from '@angular/common/http';

const serverConfig: ApplicationConfig = {
  providers: [
    provideServerRendering(),
    provideHttpClient()
  ]
};

export const config = mergeApplicationConfig({
  providers: [
    provideHttpClient()
  ]
}, serverConfig);