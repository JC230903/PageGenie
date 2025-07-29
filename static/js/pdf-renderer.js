/**
 * PDF Renderer - Handles PDF.js integration for rendering original PDF pages
 * This can be used for comparison or reference views
 */

class PDFRenderer {
    constructor() {
        this.pdfDoc = null;
        this.scale = 1.5;
        this.rotation = 0;
        
        // Set PDF.js worker source
        if (typeof pdfjsLib !== 'undefined') {
            pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';
        }
    }
    
    async loadPDF(url) {
        if (typeof pdfjsLib === 'undefined') {
            console.error('PDF.js not loaded');
            return null;
        }
        
        try {
            const loadingTask = pdfjsLib.getDocument(url);
            this.pdfDoc = await loadingTask.promise;
            console.log('PDF loaded successfully, pages:', this.pdfDoc.numPages);
            return this.pdfDoc;
        } catch (error) {
            console.error('Error loading PDF:', error);
            return null;
        }
    }
    
    async renderPage(pageNumber, canvas) {
        if (!this.pdfDoc) {
            console.error('PDF document not loaded');
            return;
        }
        
        try {
            const page = await this.pdfDoc.getPage(pageNumber);
            const viewport = page.getViewport({ scale: this.scale, rotation: this.rotation });
            
            // Prepare canvas
            const context = canvas.getContext('2d');
            canvas.height = viewport.height;
            canvas.width = viewport.width;
            
            // Render page
            const renderContext = {
                canvasContext: context,
                viewport: viewport
            };
            
            await page.render(renderContext).promise;
            console.log(`Page ${pageNumber} rendered successfully`);
            
        } catch (error) {
            console.error(`Error rendering page ${pageNumber}:`, error);
        }
    }
    
    async getTextContent(pageNumber) {
        if (!this.pdfDoc) {
            console.error('PDF document not loaded');
            return '';
        }
        
        try {
            const page = await this.pdfDoc.getPage(pageNumber);
            const textContent = await page.getTextContent();
            
            let text = '';
            textContent.items.forEach(item => {
                text += item.str + ' ';
            });
            
            return text.trim();
            
        } catch (error) {
            console.error(`Error getting text content for page ${pageNumber}:`, error);
            return '';
        }
    }
    
    setScale(scale) {
        this.scale = scale;
    }
    
    setRotation(rotation) {
        this.rotation = rotation;
    }
    
    getTotalPages() {
        return this.pdfDoc ? this.pdfDoc.numPages : 0;
    }
}

// Create a global instance for use by other components
window.PDFRenderer = PDFRenderer;

// Utility functions for PDF rendering
window.PDFUtils = {
    // Create a comparison view between original PDF and enhanced book
    createComparisonView: async function(pdfUrl, pageNumber, targetElement) {
        const renderer = new PDFRenderer();
        await renderer.loadPDF(pdfUrl);
        
        const canvas = document.createElement('canvas');
        canvas.style.maxWidth = '100%';
        canvas.style.height = 'auto';
        canvas.style.border = '1px solid var(--bs-border-color)';
        
        await renderer.renderPage(pageNumber, canvas);
        
        targetElement.innerHTML = '';
        targetElement.appendChild(canvas);
        
        return canvas;
    },
    
    // Extract text for search functionality
    extractAllText: async function(pdfUrl) {
        const renderer = new PDFRenderer();
        const pdfDoc = await renderer.loadPDF(pdfUrl);
        
        if (!pdfDoc) return '';
        
        let allText = '';
        for (let i = 1; i <= pdfDoc.numPages; i++) {
            const pageText = await renderer.getTextContent(i);
            allText += `Page ${i}:\n${pageText}\n\n`;
        }
        
        return allText;
    },
    
    // Create thumbnail previews
    createThumbnail: async function(pdfUrl, pageNumber, size = 150) {
        const renderer = new PDFRenderer();
        renderer.setScale(size / 400); // Adjust scale for thumbnail size
        
        await renderer.loadPDF(pdfUrl);
        
        const canvas = document.createElement('canvas');
        canvas.style.width = `${size}px`;
        canvas.style.height = 'auto';
        canvas.style.cursor = 'pointer';
        canvas.style.border = '2px solid transparent';
        canvas.style.borderRadius = '4px';
        canvas.style.transition = 'border-color 0.3s ease';
        
        canvas.addEventListener('mouseenter', () => {
            canvas.style.borderColor = 'var(--bs-primary)';
        });
        
        canvas.addEventListener('mouseleave', () => {
            canvas.style.borderColor = 'transparent';
        });
        
        await renderer.renderPage(pageNumber, canvas);
        
        return canvas;
    }
};

// Enhanced PDF viewer component (for future use)
class EnhancedPDFViewer {
    constructor(container, options = {}) {
        this.container = container;
        this.options = {
            showThumbnails: options.showThumbnails || false,
            enableSearch: options.enableSearch || false,
            enableDownload: options.enableDownload || false,
            ...options
        };
        
        this.renderer = new PDFRenderer();
        this.currentPage = 1;
        
        this.init();
    }
    
    init() {
        this.createViewerStructure();
        this.setupEventListeners();
    }
    
    createViewerStructure() {
        this.container.innerHTML = `
            <div class="pdf-viewer-controls mb-3">
                <div class="btn-group" role="group">
                    <button type="button" class="btn btn-outline-secondary" id="prevPageBtn">
                        <i class="fas fa-chevron-left"></i>
                    </button>
                    <button type="button" class="btn btn-outline-secondary" id="nextPageBtn">
                        <i class="fas fa-chevron-right"></i>
                    </button>
                </div>
                <span class="mx-3" id="pageInfo">Page 1 of 1</span>
                <div class="btn-group" role="group">
                    <button type="button" class="btn btn-outline-secondary" id="zoomOutBtn">
                        <i class="fas fa-search-minus"></i>
                    </button>
                    <button type="button" class="btn btn-outline-secondary" id="zoomInBtn">
                        <i class="fas fa-search-plus"></i>
                    </button>
                </div>
            </div>
            <div class="pdf-viewer-content" style="overflow: auto; max-height: 600px;">
                <canvas id="pdfCanvas"></canvas>
            </div>
        `;
    }
    
    setupEventListeners() {
        document.getElementById('prevPageBtn').addEventListener('click', () => this.previousPage());
        document.getElementById('nextPageBtn').addEventListener('click', () => this.nextPage());
        document.getElementById('zoomInBtn').addEventListener('click', () => this.zoomIn());
        document.getElementById('zoomOutBtn').addEventListener('click', () => this.zoomOut());
    }
    
    async loadPDF(url) {
        await this.renderer.loadPDF(url);
        await this.renderCurrentPage();
        this.updateControls();
    }
    
    async renderCurrentPage() {
        const canvas = document.getElementById('pdfCanvas');
        await this.renderer.renderPage(this.currentPage, canvas);
    }
    
    updateControls() {
        const totalPages = this.renderer.getTotalPages();
        document.getElementById('pageInfo').textContent = `Page ${this.currentPage} of ${totalPages}`;
        
        document.getElementById('prevPageBtn').disabled = this.currentPage <= 1;
        document.getElementById('nextPageBtn').disabled = this.currentPage >= totalPages;
    }
    
    async previousPage() {
        if (this.currentPage > 1) {
            this.currentPage--;
            await this.renderCurrentPage();
            this.updateControls();
        }
    }
    
    async nextPage() {
        if (this.currentPage < this.renderer.getTotalPages()) {
            this.currentPage++;
            await this.renderCurrentPage();
            this.updateControls();
        }
    }
    
    async zoomIn() {
        this.renderer.setScale(this.renderer.scale * 1.2);
        await this.renderCurrentPage();
    }
    
    async zoomOut() {
        this.renderer.setScale(this.renderer.scale * 0.8);
        await this.renderCurrentPage();
    }
}

window.EnhancedPDFViewer = EnhancedPDFViewer;
