# 🖼️ Property Image Upload Guide

This guide explains how to upload and manage images for your vacation rental properties.

## 📁 **Image Storage Structure**

```
static/
└── images/
    └── properties/
        ├── property_1_abc123.jpg
        ├── property_2_def456.png
        └── ...
```

## 🚀 **Quick Start Options**

### **Option 1: Web Interface (Recommended for beginners)**

1. **Access the Image Manager**
   - Go to your main site: `http://127.0.0.1:8000`
   - Click on "Image Manager" in the navigation
   - Or directly visit: `http://127.0.0.1:8000/image-manager`

2. **Upload Images**
   - Drag & drop images onto the upload area
   - Or click to browse and select multiple images
   - Assign each image to a specific property
   - Images are automatically uploaded and linked

### **Option 2: Command Line Script (Recommended for bulk uploads)**

1. **Run the bulk upload script**
   ```bash
   python bulk_upload_images.py
   ```

2. **Choose option 2: "Upload images from directory"**
3. **Enter the path to your images folder**
4. **The script will automatically assign images to properties**

## 📋 **Supported Image Formats**

- **JPG/JPEG** - Best for photos
- **PNG** - Good for graphics with transparency
- **GIF** - Animated images
- **WebP** - Modern web format

## 📏 **File Size Limits**

- **Maximum file size**: 5MB per image
- **Recommended size**: 1-3MB for optimal performance
- **Image dimensions**: Will be automatically resized to fit the display

## 🎯 **How Image Assignment Works**

### **Automatic Assignment (Bulk Upload)**
- Images are randomly assigned to properties without images
- Each property gets one image
- If you have more images than properties, some images won't be used

### **Manual Assignment (Web Interface)**
- Upload images one by one
- Choose which property each image belongs to
- Perfect for when you want specific images for specific properties

## 🔧 **Technical Details**

### **File Naming Convention**
Images are automatically renamed using this format:
```
property_{property_id}_{random_hash}.{extension}
```

Example: `property_123_a1b2c3d4.jpg`

### **Database Updates**
When you upload an image:
1. Image file is saved to `static/images/properties/`
2. Database is updated with the image URL
3. Property card automatically displays the new image

### **Image Removal**
- Use the "Remove" button in the web interface
- Or manually delete from database (not recommended)
- Removed images are permanently deleted from the server

## 📊 **Monitoring Progress**

### **Check Current Status**
```bash
python bulk_upload_images.py
# Choose option 1: "Show current image status"
```

### **Web Interface Status**
- The Image Manager shows which properties have images
- Green checkmarks indicate properties with local images
- Red X marks indicate properties without images

## 🚨 **Troubleshooting**

### **Common Issues**

1. **"File too large" error**
   - Compress your images to under 5MB
   - Use online tools like TinyPNG or ImageOptim

2. **"File not found" error**
   - Check the file path is correct
   - Ensure the file exists and is readable

3. **Images not displaying**
   - Check browser console for errors
   - Verify the image file exists in the correct directory
   - Ensure the database has the correct image URL

### **Reset All Images**
If you want to start over:
```bash
# Remove all local images
rm -rf static/images/properties/*

# Reset database (this will remove all image references)
python -c "
import sqlite3
conn = sqlite3.connect('vacation_rentals.db')
cursor = conn.cursor()
cursor.execute('UPDATE properties SET image_url = NULL, image_alt = NULL')
conn.commit()
conn.close()
print('All image references cleared')
"
```

## 💡 **Best Practices**

### **Image Preparation**
1. **Resize images** to reasonable dimensions (1200x800 pixels is good)
2. **Compress files** to reduce size while maintaining quality
3. **Use descriptive filenames** to make assignment easier
4. **Organize images** in folders by property type or location

### **Upload Strategy**
1. **Start with bulk upload** for efficiency
2. **Use web interface** for final adjustments
3. **Test a few images first** before uploading everything
4. **Keep backups** of your original images

### **Performance Tips**
1. **Upload during off-peak hours** if you have many images
2. **Use wired connection** for large uploads
3. **Close other applications** to free up system resources
4. **Monitor upload progress** to catch any errors

## 🔗 **API Endpoints**

If you want to integrate with other systems:

- **Upload image**: `POST /api/upload_property_image`
- **Remove image**: `DELETE /api/remove_property_image/{property_id}`
- **Get image status**: `GET /api/property_images`

## 📞 **Need Help?**

If you encounter issues:

1. Check the browser console for error messages
2. Look at the server logs for backend errors
3. Verify your image files are valid and accessible
4. Ensure you have proper permissions for the upload directory

## 🎉 **Success Indicators**

You'll know everything is working when:
- ✅ All properties show images instead of placeholders
- ✅ Image Manager shows 100% coverage
- ✅ Property cards display your custom images
- ✅ No more Unsplash placeholder images

Happy uploading! 🖼️✨
