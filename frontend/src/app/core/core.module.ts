import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MenuComponent } from './menu/menu.component';
import { HomeComponent } from './home/home.component';
import { FooterComponent } from './footer/footer.component';
import { SharedModule } from '../shared/shared.module';
import { RouterModule } from '@angular/router';

@NgModule({
    declarations: [MenuComponent, HomeComponent, FooterComponent],
    imports: [CommonModule, SharedModule, RouterModule],
    exports: [MenuComponent, HomeComponent, FooterComponent],
})
export class CoreModule {}
