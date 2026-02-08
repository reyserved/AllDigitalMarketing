# Figma Background Overlay Implementation Guide

## Creating Subtle Background Image Overlays

### Step 1: Set Up Your Section Frame
1. Create a **Frame** for your section (e.g., "Benefits Section")
2. Set the fill to your background color (`#F5F7FA` for off-white)
3. Enable **Clip content** in the Frame settings

---

### Step 2: Add the Background Image Layer

1. **Import your image** (drag into Figma or File > Place Image)
2. Position the image **inside the section frame**
3. Resize to cover the entire frame:
   - Set width/height to match the frame OR
   - Use **Fill** constraint in the image settings
4. **Send to back**: Right-click > Send to Back (or `Cmd + [`)

---

### Step 3: Apply Opacity (Transparency)

1. Select the image layer
2. In the **Design** panel on the right, find **Layer**
3. Set opacity:
   - `8%` for subtle campus aerial view
   - `10%` for thermoformed plastic texture
   - Adjust to taste (5-15% range works best)

---

### Step 4: Add Gradient Fade Overlay (Optional)

For a professional edge fade effect:

1. Create a **Rectangle** over the image
2. Match the size of your section frame
3. **Fill**: Set to **Linear Gradient**
4. Configure the gradient:

**Bottom Fade (Benefits Section)**:
- Stop 1: `#F5F7FA` at 100% opacity, position 0%
- Stop 2: `#F5F7FA` at 0% opacity, position 50%
- Angle: 0° (bottom to top)

**Side Fade (Process Section)**:
- Stop 1: `#F5F7FA` at 100% opacity, position 0%
- Stop 2: `#F5F7FA` at 0% opacity, position 30%
- Stop 3: `#F5F7FA` at 0% opacity, position 70%
- Stop 4: `#F5F7FA` at 100% opacity, position 100%
- Angle: 90° (left to right)

5. Position this gradient rectangle **above** the image but **below** the content

---

### Step 5: Layer Order (Bottom to Top)
```
1. Section Background (solid fill)
2. Background Image (low opacity)
3. Gradient Overlay (optional fade)
4. Content (cards, text, etc.)
```

---

## Quick Visual Reference

### Benefits Section Setup
| Layer | Settings |
|-------|----------|
| Frame | Fill: `#F5F7FA`, Clip content: ON |
| Campus Image | Opacity: 8%, Fill constraint |
| Gradient | Bottom fade, `#F5F7FA` → transparent |
| Benefit Cards | Auto Layout, positioned on top |

### Process Section Setup
| Layer | Settings |
|-------|----------|
| Frame | Fill: `#F5F7FA`, Clip content: ON |
| Plastic Image | Opacity: 10%, Cover |
| Gradient | Side fades from both edges |
| Process Steps | Auto Layout, on top |

---

## Pro Tips

1. **Use Effects for Blur**: Add a subtle **Background Blur** (4-8px) to soften the image
2. **Grayscale Option**: Add a **Color** effect set to `#808080` at 30-50% to desaturate
3. **Group Backgrounds**: Create a group called "Background Layers" and lock it to prevent accidental edits
4. **Component It**: Turn your background setup into a reusable component

---

## Image URLs

- **Campus Aerial**: `https://www.fivestarfabricating.com/wp-content/uploads/2024/03/Innovative-Products-Since-1978-Campus-Version-2.jpg`
- **Thermoformed Plastic**: `https://www.fivestarfabricating.com/wp-content/uploads/2024/03/Thermoformed-Plastic-v2-1.jpg`

---

## Hero Section Background Overlay (Dark Background)

For applying a subtle image overlay on the navy hero section:

### Step 1: Set Up Hero Frame
1. Create your hero frame with fill: `#263380` (navy)
2. Set frame height to approximately 85vh (~600-700px)
3. Enable **Clip content**

### Step 2: Add Background Image Layer
1. Import the **Thermoformed Plastic** image
2. Position it on the **right side** of the hero
3. Resize to cover about 60% width of the hero (from right edge)
4. Make sure it covers the full height

### Step 3: Apply Opacity
1. Select the image
2. Set **Layer opacity** to `15%` in the Design panel

### Step 4: Create Gradient Fade (Critical!)
1. Create a **Rectangle** on top of the image, same size
2. Fill with **Linear Gradient**:
   - Stop 1: `#263380` at 100% opacity, position 0% (left)
   - Stop 2: `#263380` at 70% opacity, position 30%
   - Stop 3: `#263380` at 0% opacity, position 100% (right)
3. Angle: 90° (left to right)

### Step 5: Add Navy Gradient Overlay
1. Create another rectangle covering the **entire hero**
2. Fill with **Linear Gradient**:
   - Stop 1: `rgba(38, 51, 128, 0.95)` position 0%
   - Stop 2: `rgba(26, 36, 86, 0.85)` position 100%
3. Angle: 135° (diagonal)
4. This adds depth over the image

### Step 6: Add Gold Glow Accent (Optional)
1. Create a large **Ellipse** positioned top-right, extending outside the frame
2. Fill with **Radial Gradient**:
   - Center: `rgba(212, 175, 55, 0.1)` (gold at 10%)
   - Edge: `transparent`
3. Set blend mode to **Normal** or **Screen**

### Step 7: Layer Order (Bottom to Top)
```
1. Hero Frame (navy fill #263380)
2. Thermoformed Plastic Image (15% opacity, right-aligned)
3. Gradient Rectangle (fades image on left)
4. Navy Gradient Overlay (full hero)
5. Gold Glow Ellipse (top-right accent)
6. Hero Content (text, form, badges)
```

### Quick Reference Table
| Layer | Opacity | Position | Purpose |
|-------|---------|----------|---------|
| Navy Fill | 100% | Base | Primary background |
| Plastic Image | 15% | Right 60% | Industrial texture |
| Fade Gradient | 100% | Over image | Blends image to navy |
| Navy Overlay | 95-85% | Full | Adds depth |
| Gold Glow | 10% | Top-right | Warm accent |

### Pro Tips for Hero Overlays
1. **Don't overdo opacity** - 10-15% is plenty for dark backgrounds
2. **Always add gradient fade** - Prevents the image from competing with text
3. **Group all background layers** - Name it "Hero Background" and lock it
4. **Test with content** - Ensure text remains readable over the overlay
