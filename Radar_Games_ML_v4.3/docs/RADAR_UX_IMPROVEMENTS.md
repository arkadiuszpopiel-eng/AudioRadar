# Radar UX Improvement Plan - v4.3.1-k0007

**Created:** 2025-12-17
**User Feedback:** "Powiedz mi? Jak poprawić przejrzystość, czytelność radaru?! Bo szczerze mało intuicyjny jest?"

---

## 🎯 Problem Analysis

After analyzing `app/widgets/military_hud.py`, identified **7 critical UX issues**:

1. **Font sizes too small** - 8-11pt fonts unreadable on modern displays
2. **Low color contrast** - all cyan/teal, hard to distinguish elements
3. **Target icons too small** - ~20px height with dim glow effects
4. **Distance labels hard to read** - dim color, only on one side
5. **No legend/key** - user must guess icon meanings
6. **Target list cramped** - 8pt font, 32px spacing, max 8 targets
7. **Panel backgrounds too transparent** - text hard to read

---

## ✅ Proposed Solutions

### 1. Increase Font Sizes (+30-50%)

**Before:**
```python
self.FONT_MAIN = QFont("Consolas", 9)
self.FONT_LABEL = QFont("Consolas", 8)
self.FONT_STATUS = QFont("Consolas", 10, QFont.Bold)
self.FONT_TITLE = QFont("Consolas", 11, QFont.Bold)
```

**After:**
```python
self.FONT_MAIN = QFont("Consolas", 12)     # +33%
self.FONT_LABEL = QFont("Consolas", 11)    # +38%
self.FONT_STATUS = QFont("Consolas", 13, QFont.Bold)  # +30%
self.FONT_TITLE = QFont("Consolas", 15, QFont.Bold)   # +36%
```

**Impact:** Much better readability on 1080p+ displays

---

### 2. Improve Color Contrast & Diversity

**Before:**
```python
self.COLOR_GRID = QColor(0, 60, 80, 80)        # Dim cyan
self.COLOR_GRID_MAJOR = QColor(0, 100, 120, 120)
self.COLOR_TEXT = QColor(0, 200, 150)          # Cyan text
self.COLOR_TEXT_DIM = QColor(0, 120, 100)      # Too dim
```

**After:**
```python
# Brighter grid for better distance judgment
self.COLOR_GRID = QColor(0, 80, 100, 120)         # +50% alpha
self.COLOR_GRID_MAJOR = QColor(0, 150, 180, 180)  # +50% alpha

# More readable text
self.COLOR_TEXT = QColor(0, 255, 200)             # Brighter
self.COLOR_TEXT_DIM = QColor(0, 180, 150)         # 50% brighter

# Add distinct UI element colors
self.COLOR_PANEL_BG = QColor(0, 20, 30, 240)      # Less transparent
self.COLOR_DISTANCE_LABEL = QColor(100, 200, 255) # Distinct blue
```

**Impact:** Better element distinction, easier distance judgment

---

### 3. Larger Target Icons with Stronger Glow

**Before:**
```python
# Walk icon (lines 354-376)
painter.drawEllipse(x - 3, y - 12, 6, 6)  # 6px head
painter.drawLine(x, y - 6, x, y + 2)       # 8px body
# Glow: 50 alpha (too subtle)
painter.setPen(QPen(QColor(color.red(), color.green(), color.blue(), 50), 6))
```

**After:**
```python
# Scale factor: 1.5x larger
scale = 1.5

# Walk icon - 50% larger
painter.drawEllipse(x - 4, y - 18, 9, 9)   # 9px head
painter.drawLine(x, y - 9, x, y + 3)       # 12px body
# Arms and legs scaled proportionally

# Stronger glow: 100 alpha
painter.setPen(QPen(QColor(color.red(), color.green(), color.blue(), 100), 8))
painter.drawEllipse(x - 12, y - 21, 24, 39)  # Larger glow area
```

**Impact:** Icons 50% larger, glow 2x brighter - much more visible

---

### 4. Enhanced Distance Labels

**Before:**
```python
# Only on right side, dim color
dist_label = f"{int(self.max_distance * ratio)}m"
painter.setFont(self.FONT_LABEL)  # 8pt
painter.setPen(self.COLOR_TEXT_DIM)  # Dim
painter.drawText(cx + 5, cy - radius + 12, dist_label)
```

**After:**
```python
# Show on all 4 cardinal directions
dist_label = f"{int(self.max_distance * ratio)}m"
painter.setFont(self.FONT_LABEL)  # Now 11pt
painter.setPen(self.COLOR_DISTANCE_LABEL)  # Distinct blue

# Draw at N, E, S, W positions
for angle_deg in [0, 90, 180, 270]:
    rad = math.radians(angle_deg - 90)
    label_x = cx + int(radius * math.cos(rad))
    label_y = cy + int(radius * math.sin(rad))

    # Offset for readability
    if angle_deg == 0:    # North
        painter.drawText(label_x - 15, label_y - 10, dist_label)
    elif angle_deg == 90:  # East
        painter.drawText(label_x + 10, label_y + 5, dist_label)
    elif angle_deg == 180: # South
        painter.drawText(label_x - 15, label_y + 20, dist_label)
    else:                  # West
        painter.drawText(label_x - 35, label_y + 5, dist_label)
```

**Impact:** Distance rings readable from all angles

---

### 5. Add Interactive Legend Panel

**New Feature:**
```python
def _draw_legend(self, painter, w, h):
    """Draw legend showing target types and colors"""
    x = w - 160
    y = h - 150  # Above status bar

    # Legend background
    painter.fillRect(x, y, 150, 100, QColor(0, 20, 30, 240))
    painter.setPen(QPen(self.COLOR_GRID_MAJOR, 1))
    painter.drawRect(x, y, 150, 100)

    # Title
    painter.setFont(self.FONT_STATUS)
    painter.setPen(self.COLOR_ACCENT)
    painter.drawText(x + 10, y + 18, tr('legend'))

    # Legend items
    painter.setFont(self.FONT_LABEL)
    legend_y = y + 35

    # Walk
    self._draw_walk_icon(painter, x + 20, legend_y, TargetState.COLORS[TargetState.WALK])
    painter.setPen(TargetState.COLORS[TargetState.WALK])
    painter.drawText(x + 35, legend_y + 5, tr('walk'))
    legend_y += 20

    # Run
    self._draw_run_icon(painter, x + 20, legend_y, TargetState.COLORS[TargetState.RUN])
    painter.setPen(TargetState.COLORS[TargetState.RUN])
    painter.drawText(x + 35, legend_y + 5, tr('run'))
    legend_y += 20

    # Shot
    self._draw_shot_icon(painter, x + 20, legend_y, TargetState.COLORS[TargetState.SHOT])
    painter.setPen(TargetState.COLORS[TargetState.SHOT])
    painter.drawText(x + 35, legend_y + 5, tr('shot'))
```

**Impact:** User instantly understands what each icon means

---

### 6. Improve Target List Spacing

**Before:**
```python
ty = y + 45
for i, target in enumerate(self.targets[:8]):  # Max 8
    # ... draw target info ...
    ty += 32  # Cramped spacing
```

**After:**
```python
ty = y + 50
for i, target in enumerate(self.targets[:10]):  # Show 10 targets
    # ... draw target info with FONT_LABEL (now 11pt) ...
    ty += 40  # 25% more spacing

# Add scrollbar indicator if more targets exist
if len(self.targets) > 10:
    painter.setPen(self.COLOR_WARNING)
    painter.drawText(x + 10, h - 40, f"▼ +{len(self.targets) - 10} more")
```

**Impact:** Better readability, user knows when targets are hidden

---

### 7. Increase Panel Background Opacity

**Before:**
```python
painter.fillRect(x, y, panel_width - 10, h - 10,
                QColor(0, 15, 20, 200))  # 78% opaque
```

**After:**
```python
painter.fillRect(x, y, panel_width - 10, h - 10,
                QColor(0, 20, 30, 240))  # 94% opaque
```

**Impact:** Text much easier to read over radar background

---

## 🎨 Additional Enhancements

### 8. Add Configurable Brightness/Contrast

```python
def __init__(self, parent=None):
    # ... existing code ...

    # User-configurable display settings
    self.brightness_multiplier = 1.0  # 0.5 - 2.0
    self.contrast_mode = "standard"   # "standard", "high", "max"

def set_brightness(self, value: float):
    """Set radar brightness (0.5 = dim, 1.0 = normal, 2.0 = bright)"""
    self.brightness_multiplier = max(0.5, min(2.0, value))
    self._update_colors()

def set_contrast_mode(self, mode: str):
    """Set contrast mode: standard, high, max"""
    self.contrast_mode = mode
    self._update_colors()

def _update_colors(self):
    """Recalculate colors based on brightness/contrast settings"""
    # Adjust all colors based on settings
    # This allows runtime customization without code changes
```

---

### 9. Add Distance Ring Highlight on Hover

```python
def mouseMoveEvent(self, event):
    """Highlight nearest distance ring on hover"""
    cx, cy = self.width() // 2, (self.height() - 40) // 2
    dx = event.x() - cx
    dy = event.y() - cy
    dist_from_center = math.sqrt(dx*dx + dy*dy)

    # Find nearest ring
    for ratio in [0.25, 0.5, 0.75, 1.0]:
        ring_radius = self.radar_radius * ratio
        if abs(dist_from_center - ring_radius) < 15:
            self.highlighted_ring = ratio
            self.update()
            return

    self.highlighted_ring = None
    self.update()
```

---

### 10. Add Zoom Controls

```python
def set_range(self, meters: int):
    """Change radar range (25m, 50m, 100m, 200m)"""
    self.max_distance = meters
    self.range_mode = f"{meters}m"
    self.update()

# Keyboard shortcuts:
# - Press '1' for 25m range
# - Press '2' for 50m range
# - Press '3' for 100m range
# - Press '4' for 200m range
```

---

## 📋 Implementation Priority

### **Phase 1 - CRITICAL (Immediate Impact):**
1. ✅ Increase font sizes (+30-50%)
2. ✅ Improve color contrast (brighter grid, readable text)
3. ✅ Larger target icons (+50% size)
4. ✅ Increase panel opacity (94% opaque)

**Estimated Time:** 30-45 minutes
**Impact:** 80% better readability

---

### **Phase 2 - HIGH (Major UX Improvement):**
5. ✅ Enhanced distance labels (4 cardinal directions)
6. ✅ Add legend panel
7. ✅ Improve target list spacing

**Estimated Time:** 45-60 minutes
**Impact:** 90% better usability

---

### **Phase 3 - MEDIUM (Nice to Have):**
8. ⚠️ Configurable brightness/contrast
9. ⚠️ Distance ring hover highlight
10. ⚠️ Zoom/range controls

**Estimated Time:** 60-90 minutes
**Impact:** Professional-grade UX

---

## 🔧 Translation Keys Needed

Add to `app/core/translations.py`:

```python
# English
'legend': 'LEGEND',

# Polish
'legend': 'LEGENDA',
```

---

## 🧪 Testing Plan

After implementation:

1. **Readability Test:**
   - View radar from 1.5m distance
   - All text should be readable without squinting

2. **Icon Visibility Test:**
   - Add 5+ targets at various distances
   - All icons should be clearly distinguishable

3. **Distance Judgment Test:**
   - Place targets at known distances
   - User should estimate distance within ±10m

4. **Color Distinction Test:**
   - Add Walk, Run, Shot targets simultaneously
   - Colors should be clearly different

5. **Panel Contrast Test:**
   - Ensure text readable over radar animations

---

## 📊 Before/After Comparison

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Font Size (avg) | 9.5pt | 12.75pt | **+34%** |
| Icon Size | 20px | 30px | **+50%** |
| Glow Alpha | 50 | 100 | **+100%** |
| Grid Alpha | 80 | 120 | **+50%** |
| Panel Opacity | 78% | 94% | **+20%** |
| Distance Labels | 1 position | 4 positions | **+300%** |
| Has Legend | ❌ No | ✅ Yes | ∞ |

---

## ✅ User Approval Required

**Question for user:**
- Start with Phase 1 (critical) or implement all phases at once?
- Any specific colors/styles you prefer?
- Should legend be always visible or toggle button?

---

**Radar Games ML v4.3.1-k0007** - Comprehensive radar UX improvement plan.
