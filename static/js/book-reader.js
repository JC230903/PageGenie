/**
 * Book Reader JavaScript - Handles the interactive book interface
 */

class BookReader {
    constructor() {
        this.bookData = null;
        this.currentSpread = 0; // Current two-page spread (0 = pages 1-2, 1 = pages 3-4, etc.)
        this.totalSpreads = 0;
        this.isAnimating = false;
        
        this.init();
    }
    
    init() {
        // Load book data from the embedded JSON
        const bookDataElement = document.getElementById('bookData');
        if (bookDataElement) {
            try {
                this.bookData = JSON.parse(bookDataElement.textContent);
                this.totalSpreads = Math.ceil(this.bookData.total_pages / 2);
                this.setupEventListeners();
                this.renderCurrentSpread();
            } catch (error) {
                console.error('Error parsing book data:', error);
                this.showError('Failed to load book data');
            }
        } else {
            console.error('Book data not found');
            this.showError('Book data not available');
        }
    }
    
    setupEventListeners() {
        // Navigation buttons
        document.getElementById('prevBtn').addEventListener('click', () => this.previousSpread());
        document.getElementById('nextBtn').addEventListener('click', () => this.nextSpread());
        
        // Keyboard navigation
        document.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowLeft') this.previousSpread();
            if (e.key === 'ArrowRight') this.nextSpread();
        });
        
        // Swipe gestures for mobile
        this.setupSwipeGestures();
    }
    
    setupSwipeGestures() {
        let startX = 0;
        let startY = 0;
        
        const bookViewer = document.getElementById('bookViewer');
        
        bookViewer.addEventListener('touchstart', (e) => {
            startX = e.touches[0].clientX;
            startY = e.touches[0].clientY;
        }, { passive: true });
        
        bookViewer.addEventListener('touchend', (e) => {
            const endX = e.changedTouches[0].clientX;
            const endY = e.changedTouches[0].clientY;
            
            const deltaX = endX - startX;
            const deltaY = endY - startY;
            
            // Check if horizontal swipe is more significant than vertical
            if (Math.abs(deltaX) > Math.abs(deltaY) && Math.abs(deltaX) > 50) {
                if (deltaX > 0) {
                    this.previousSpread();
                } else {
                    this.nextSpread();
                }
            }
        }, { passive: true });
    }
    
    renderCurrentSpread() {
        if (this.isAnimating) return;
        
        const leftPageIndex = this.currentSpread * 2;
        const rightPageIndex = leftPageIndex + 1;
        
        // Update page info
        this.updatePageInfo();
        
        // Update navigation buttons
        this.updateNavigationButtons();
        
        // Render pages
        this.renderPage('left', leftPageIndex);
        this.renderPage('right', rightPageIndex);
        
        // Add marginalia after a short delay to ensure page content is rendered
        setTimeout(() => {
            this.renderMarginalia('left', leftPageIndex);
            this.renderMarginalia('right', rightPageIndex);
        }, 100);
    }
    
    renderPage(side, pageIndex) {
        const pageElement = document.getElementById(`${side}Page`);
        const contentElement = document.getElementById(`${side}PageContent`);
        const numberElement = document.getElementById(`${side}PageNumber`);
        const textElement = document.getElementById(`${side}PageText`);
        
        // Clear previous content
        textElement.innerHTML = '';
        numberElement.textContent = '';
        
        // Check if page exists
        if (pageIndex >= this.bookData.pages.length) {
            pageElement.style.visibility = 'hidden';
            return;
        }
        
        pageElement.style.visibility = 'visible';
        const pageData = this.bookData.pages[pageIndex];
        
        // Set page number
        numberElement.textContent = pageData.page_number;
        
        // Set page content
        this.renderPageText(textElement, pageData.text_content);
        
        // Apply theme styling
        this.applyPageTheme(pageElement, pageData);
    }
    
    renderPageText(textElement, textContent) {
        if (!textContent) {
            textElement.innerHTML = '<p class="text-muted text-center mt-5">No content available for this page.</p>';
            return;
        }
        
        // Split text into paragraphs and format
        const paragraphs = textContent.split('\n\n').filter(p => p.trim());
        
        paragraphs.forEach(paragraph => {
            const p = document.createElement('p');
            p.textContent = paragraph.trim();
            textElement.appendChild(p);
        });
        
        // If no paragraphs were created, add the raw text
        if (paragraphs.length === 0) {
            const p = document.createElement('p');
            p.textContent = textContent;
            textElement.appendChild(p);
        }
    }
    
    applyPageTheme(pageElement, pageData) {
        // Remove existing theme classes
        pageElement.classList.remove('fantasy-theme', 'scifi-theme', 'mystery-theme');
        
        // Apply theme based on genre or mood
        const genre = this.bookData.genre.toLowerCase();
        if (genre.includes('fantasy')) {
            pageElement.classList.add('fantasy-theme');
        } else if (genre.includes('science') || genre.includes('sci-fi')) {
            pageElement.classList.add('scifi-theme');
        } else if (genre.includes('mystery')) {
            pageElement.classList.add('mystery-theme');
        }
    }
    
    renderMarginalia(side, pageIndex) {
        const marginaliaContainer = document.getElementById(`${side}Marginalia`);
        
        // Clear previous marginalia
        marginaliaContainer.innerHTML = '';
        
        // Check if page exists
        if (pageIndex >= this.bookData.pages.length) {
            return;
        }
        
        const pageData = this.bookData.pages[pageIndex];
        
        if (!pageData.marginalia || pageData.marginalia.length === 0) {
            return;
        }
        
        // Add marginalia items
        pageData.marginalia.forEach((marginalia, index) => {
            const marginaliaElement = this.createMarginaliaElement(marginalia, index);
            marginaliaContainer.appendChild(marginaliaElement);
        });
    }
    
    createMarginaliaElement(marginalia, index) {
        const element = document.createElement('div');
        element.className = 'marginalia-item';
        element.style.left = `${marginalia.position_x}%`;
        element.style.top = `${marginalia.position_y}%`;
        element.style.width = `${marginalia.width}px`;
        element.style.height = `${marginalia.height}px`;
        
        // Create image element
        const img = document.createElement('img');
        img.src = marginalia.image_url;
        img.alt = `Marginalia: ${marginalia.theme}`;
        img.title = `Theme: ${marginalia.theme}`;
        
        // Handle image loading
        img.onload = () => {
            // Fade in the marginalia with a staggered delay
            setTimeout(() => {
                element.classList.add('visible');
            }, index * 200);
        };
        
        img.onerror = () => {
            // If image fails to load, create a simple placeholder
            element.innerHTML = `<div style="
                width: 100%; 
                height: 100%; 
                background: var(--bs-secondary); 
                border-radius: 4px; 
                display: flex; 
                align-items: center; 
                justify-content: center; 
                font-size: 0.7rem; 
                color: white;
                text-align: center;
            ">${marginalia.theme}</div>`;
            
            setTimeout(() => {
                element.classList.add('visible');
            }, index * 200);
        };
        
        element.appendChild(img);
        
        // Add click handler for marginalia details
        element.addEventListener('click', (e) => {
            e.stopPropagation();
            this.showMarginaliaDetails(marginalia);
        });
        
        return element;
    }
    
    showMarginaliaDetails(marginalia) {
        // Create a simple tooltip or modal for marginalia details
        const tooltip = document.createElement('div');
        tooltip.className = 'marginalia-tooltip';
        tooltip.innerHTML = `
            <div class="card bg-dark text-light" style="position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); z-index: 1000; max-width: 300px;">
                <div class="card-body">
                    <h6 class="card-title">Marginalia Details</h6>
                    <p><strong>Theme:</strong> ${marginalia.theme}</p>
                    <p><strong>Style:</strong> ${this.bookData.genre} artwork</p>
                    <button class="btn btn-sm btn-outline-light" onclick="this.parentElement.parentElement.parentElement.remove()">Close</button>
                </div>
            </div>
        `;
        
        document.body.appendChild(tooltip);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (tooltip.parentElement) {
                tooltip.remove();
            }
        }, 5000);
    }
    
    previousSpread() {
        if (this.isAnimating || this.currentSpread <= 0) return;
        
        this.animatePageTurn(() => {
            this.currentSpread--;
            this.renderCurrentSpread();
        });
    }
    
    nextSpread() {
        if (this.isAnimating || this.currentSpread >= this.totalSpreads - 1) return;
        
        this.animatePageTurn(() => {
            this.currentSpread++;
            this.renderCurrentSpread();
        });
    }
    
    animatePageTurn(callback) {
        this.isAnimating = true;
        
        // Add turning animation classes
        const leftPage = document.getElementById('leftPage');
        const rightPage = document.getElementById('rightPage');
        
        leftPage.classList.add('turning-left');
        rightPage.classList.add('turning-right');
        
        // Execute callback after animation
        setTimeout(() => {
            callback();
            
            // Remove animation classes
            leftPage.classList.remove('turning-left');
            rightPage.classList.remove('turning-right');
            
            this.isAnimating = false;
        }, 600); // Match CSS transition duration
    }
    
    updatePageInfo() {
        const pageInfoElement = document.getElementById('pageInfo');
        const leftPageNum = this.currentSpread * 2 + 1;
        const rightPageNum = Math.min(leftPageNum + 1, this.bookData.total_pages);
        
        if (leftPageNum === rightPageNum) {
            pageInfoElement.textContent = `Page ${leftPageNum} of ${this.bookData.total_pages}`;
        } else {
            pageInfoElement.textContent = `Pages ${leftPageNum}-${rightPageNum} of ${this.bookData.total_pages}`;
        }
    }
    
    updateNavigationButtons() {
        const prevBtn = document.getElementById('prevBtn');
        const nextBtn = document.getElementById('nextBtn');
        
        prevBtn.disabled = this.currentSpread <= 0;
        nextBtn.disabled = this.currentSpread >= this.totalSpreads - 1;
    }
    
    showError(message) {
        const bookViewer = document.getElementById('bookViewer');
        bookViewer.innerHTML = `
            <div class="text-center">
                <i class="fas fa-exclamation-triangle fa-3x text-warning mb-3"></i>
                <h4>Error Loading Book</h4>
                <p class="text-muted">${message}</p>
                <a href="/" class="btn btn-primary">
                    <i class="fas fa-arrow-left me-2"></i>
                    Return to Upload
                </a>
            </div>
        `;
    }
}

// Initialize the book reader when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new BookReader();
});

// Add some utility functions for enhanced interactivity
window.BookReaderUtils = {
    // Jump to a specific page
    goToPage: function(pageNumber) {
        const bookReader = window.bookReaderInstance;
        if (bookReader && pageNumber >= 1 && pageNumber <= bookReader.bookData.total_pages) {
            const spreadIndex = Math.floor((pageNumber - 1) / 2);
            bookReader.currentSpread = spreadIndex;
            bookReader.renderCurrentSpread();
        }
    },
    
    // Toggle fullscreen mode
    toggleFullscreen: function() {
        const bookViewer = document.getElementById('bookViewer');
        if (document.fullscreenElement) {
            document.exitFullscreen();
        } else {
            bookViewer.requestFullscreen();
        }
    },
    
    // Export current page as image (future enhancement)
    exportPage: function() {
        // This could be implemented to export the current page view
        console.log('Export functionality could be implemented here');
    }
};
