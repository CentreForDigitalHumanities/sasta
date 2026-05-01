/* eslint-disable @typescript-eslint/no-explicit-any */
import {
    AfterViewChecked,
    Component,
    ElementRef,
    EventEmitter,
    Input,
    OnChanges,
    OnInit,
    Output,
    SecurityContext,
    SimpleChange,
    ViewChild,
} from '@angular/core';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import {
    faArrowsAlt,
    faChevronLeft,
    faChevronRight,
    faCommentDots,
    faFileCode,
    faSearchMinus,
    faSearchPlus,
    faTimes,
} from '@fortawesome/free-solid-svg-icons';
import * as $ from 'jquery';
import { XmlParseService } from '@services';
import './tree-visualizer';

type TypedChanges = { [name in keyof TreeVisualizerComponent]: SimpleChange };
type TreeVisualizerDisplay = 'fullscreen' | 'inline' | 'both';
interface Metadata {
    name: string;
    /**
     * This can contain xml entities, display using innerHTML
     */
    value: string;
}

@Component({
    standalone: false,
    selector: 'sas-tree-visualizer',
    templateUrl: './tree-visualizer.component.html',
    styleUrls: ['./tree-visualizer.component.scss'],
})
export class TreeVisualizerComponent
implements OnInit, OnChanges, AfterViewChecked
{
    @ViewChild('output', { static: true, read: ElementRef })
    public output: ElementRef;
    @ViewChild('inline', { read: ElementRef })
    public inlineRef: ElementRef;
    @ViewChild('tree', { read: ElementRef })
    public tree: ElementRef;
    @ViewChild('metadataCard', { read: ElementRef })
    public metadataCard: ElementRef;

    @Input()
    public xml: string;

    @Input()
    public sentence: SafeHtml;

    @Input()
    public filename: string;

    @Input()
    public display: TreeVisualizerDisplay = 'inline';

    @Input()
    public fullScreenButton = true;

    @Input()
    public showMatrixDetails: boolean;

    @Input()
    public url: string;

    @Input()
    public loading = false;

    @Output()
    public displayChange = new EventEmitter<TreeVisualizerDisplay>();

    @Output()
    public closeTree = new EventEmitter<void>();

    public metadata: Metadata[] | undefined;
    public showLoader: boolean;

    // fontawesome
    faArrowsAlt = faArrowsAlt;
    faChevronLeft = faChevronLeft;
    faChevronRight = faChevronRight;
    faCommentDots = faCommentDots;
    faFileCode = faFileCode;
    faSearchPlus = faSearchPlus;
    faSearchMinus = faSearchMinus;
    faTimes = faTimes;

    // jquery tree visualizer
    private instance: any;

    constructor(
        private sanitizer: DomSanitizer,
        private xmlParseService: XmlParseService
    ) {}

    ngOnInit(): void {
        const element = $(this.output.nativeElement);
        element.on('close', () => {
            if (this.display === 'both') {
                this.displayChange.next('inline');
            }
            this.closeTree.next();
        });
    }

    ngOnChanges(changes: TypedChanges) {
        const element = $(this.output.nativeElement);
        if (changes.loading && this.loading) {
            this.showLoader = true;
        }

        if (!this.loading && this.xml) {
            if (
                changes.xml &&
                changes.xml.currentValue !== changes.xml.previousValue
            ) {
                this.visualize(element);
            }

            if (this.instance) {
                this.updateVisibility();
            }
        }
    }

    ngAfterViewChecked(): void {
        if (this.tree && this.metadataCard) {
            // make sure the metadata overview doesn't overflow
            $(this.metadataCard.nativeElement).css({
                maxHeight: $(this.tree.nativeElement).outerHeight(),
            });
        }
    }

    private visualize(element: any) {
        setTimeout(() => {
            // Make sure the visualization happens after the
            // view (which acts a placeholder) has been rendered.
            this.instance = element.treeVisualizer(this.xml, {
                nvFontSize: 14,
                sentence:
                    (this.sentence &&
                        this.sanitizer.sanitize(
                            SecurityContext.HTML,
                            this.sentence
                        )) ||
                    '',
                showMatrixDetails: this.showMatrixDetails,
            });

            this.xmlParseService.parseXml(this.xml).then((data) => {
                this.showMetadata(data);
            });
            this.updateVisibility();
        });
    }

    private updateVisibility() {
        const inline = $(this.inlineRef && this.inlineRef.nativeElement);

        if (this.display !== 'fullscreen') {
            inline.show();
        } else {
            inline.hide();
        }

        if (this.display !== 'inline') {
            this.instance.trigger('open-fullscreen');
        } else {
            this.instance.trigger('close-fullscreen');
        }

        this.showLoader = false;
    }

    /**
     * Shows the metadata of a tree.
     *
     * @param data The parsed XML data
     */
    private showMetadata(data: {
        alpino_ds: {
            metadata: {
                meta: {
                    $: {
                        name: string;
                        value: string;
                    };
                }[];
            }[];
        }[];
    }) {
        const result: Metadata[] = [];
        if (
            data &&
            data.alpino_ds &&
            data.alpino_ds.length === 1 &&
            data.alpino_ds[0].metadata &&
            data.alpino_ds[0].metadata[0].meta
        ) {
            for (const item of data.alpino_ds[0].metadata[0].meta.sort(
                (a: any, b: any) => a.$.name.localeCompare(b.$.name)
            )) {
                result.push({ name: item.$.name, value: item.$.value });
            }
        }
        this.metadata = result.length ? result : undefined;
    }
}
