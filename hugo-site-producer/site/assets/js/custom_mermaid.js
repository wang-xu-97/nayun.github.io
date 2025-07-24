// 存储所有 panzoom 实例
const panzoomInstances = new Map();

// 初始化所有 mermaid 容器
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.mermaid-zoom').forEach((container, index) => {
        const observer = new MutationObserver(mutations => {
            const svg = container.querySelector('svg');
            if (svg) {
                observer.disconnect();
                
                // 初始化 Panzoom
                initPanzoom(container, svg, index);
            }
        });
        
        observer.observe(container, { 
            childList: true, 
            subtree: true 
        });
        
        // 如果 SVG 已存在，直接初始化
        const existingSvg = container.querySelector('svg');
        if (existingSvg) {
            initPanzoom(container, existingSvg, index);
        }
    });
});

// 初始化 Panzoom 实例
function initPanzoom(container, svg, index) {
    try {
        // 创建 Panzoom 实例
        const panzoomInstance = panzoom(svg, {
            bounds: true,
            maxZoom: 5,
            minZoom: 0.2,
            smoothScroll: false,
            beforeWheel: (e) => {
                // 允许使用 Ctrl/Cmd + 滚轮缩放
                return e.ctrlKey || e.metaKey;
            }
        });
        
        // 存储实例
        panzoomInstances.set(container.id || `mermaid-container-${index}`, {
            instance: panzoomInstance,
            container: container,
            initialScale: 1
        });
        
        console.log('Panzoom initialized for', container);
    } catch (error) {
        console.error('Error initializing Panzoom:', error);
    }
}

// 缩放函数 - 使用视图中心点
window.zoomIn = function(btn, event) {
    console.log('zoomIn', btn);
    event.stopPropagation();
    const container = btn.closest('.mermaid-zoom');
    if (!container) return;
    
    const containerId = container.id || Array.from(panzoomInstances.keys()).find(key => 
        panzoomInstances.get(key).container === container
    );
    
    if (!containerId || !panzoomInstances.has(containerId)) return;
    
    const { instance } = panzoomInstances.get(containerId);
    const transform = instance.getTransform();
    
    // 计算视图中心点
    const rect = container.getBoundingClientRect();
    const centerX = rect.left + rect.width / 2;
    const centerY = rect.top + rect.height / 2;
    
    // 基于当前比例缩放
    const newScale = transform.scale * 1.2;
    instance.zoomTo(centerX, centerY, newScale);
};

window.zoomOut = function(btn, event) {
    event.stopPropagation();
    const container = btn.closest('.mermaid-zoom');
    if (!container) return;
    
    const containerId = container.id || Array.from(panzoomInstances.keys()).find(key => 
        panzoomInstances.get(key).container === container
    );
    
    if (!containerId || !panzoomInstances.has(containerId)) return;
    
    const { instance } = panzoomInstances.get(containerId);
    const transform = instance.getTransform();
    
    const rect = container.getBoundingClientRect();
    const centerX = rect.left + rect.width / 2;
    const centerY = rect.top + rect.height / 2;
    
    const newScale = transform.scale * 0.8;
    instance.zoomTo(centerX, centerY, newScale);
};

window.resetZoom = function(btn, event) {
    event.stopPropagation();
    const container = btn.closest('.mermaid-zoom');
    if (!container) return;
    
    const containerId = container.id || Array.from(panzoomInstances.keys()).find(key => 
        panzoomInstances.get(key).container === container
    );
    
    if (!containerId || !panzoomInstances.has(containerId)) return;
    
    const { instance, initialScale } = panzoomInstances.get(containerId);
    const rect = container.getBoundingClientRect();
    const centerX = rect.left + rect.width / 2;
    const centerY = rect.top + rect.height / 2;
    
    instance.zoomTo(centerX, centerY, initialScale);
};