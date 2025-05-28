# Apache Solr Core Export, Clean-up, and Import Guide

This guide outlines the complete procedure to export documents from a Solr core, clean them for import, and reload them into a new core with AI-compatible schema enhancements.

---

Goto main folder

```bash
cd /opt/solr
```

## 1️⃣ Export Data from Source Core


```bash
curl "http://localhost:8983/solr/C0018_JEW/select?q=*:*&rows=100000&wt=json" -o /var/www/SOLR_AI/exported_data.json
```

---

## 2️⃣ Prepare and Clean the Data

Extract document array from Solr response:

```bash
jq '.response.docs' /var/www/SOLR_AI/exported_data.json > /var/www/SOLR_AI/postable_docs.json
```

Remove `_version_` field to make documents importable:

```bash
jq 'map(del(._version_))' /var/www/SOLR_AI/postable_docs.json > /var/www/SOLR_AI/clean_docs.json
```

---

## 3️⃣ Recreate Target Core

Delete old core (if exists):

```bash
sudo su - solr -c "/opt/solr/bin/solr delete -c AI_NEW"
```

Create a new Solr core:

```bash
sudo su - solr -c "/opt/solr/bin/solr create -c AI_NEW"
```

---

## 4️⃣ Define Schema for AI_NEW

### Add Static & Dynamic Fields

```bash
curl -X POST -H 'Content-type:application/json' --data-binary @- http://localhost:8983/solr/AI_NEW/schema <<EOF
{
  "add-field": [
    { "name": "jew_identity", "type": "string", "multiValued": false, "stored": true },
    { "name": "jew_bundle_id", "type": "string", "multiValued": false, "stored": true },
    { "name": "jew_stock_id", "type": "string", "multiValued": false, "stored": true },
    { "name": "jew_bhub_id", "type": "string", "multiValued": false, "stored": true },
    { "name": "jew_company", "type": "string", "multiValued": false, "stored": true },
    { "name": "jew_sku", "type": "string", "multiValued": false, "stored": true },
    { "name": "jew_type", "type": "string", "multiValued": false, "stored": true },
    { "name": "jew_categories", "type": "string", "multiValued": true, "stored": true },
    { "name": "jew_title", "type": "text_general", "multiValued": false, "stored": true },
    { "name": "jew_description", "type": "string", "multiValued": false, "stored": true },
    { "name": "jew_short_description", "type": "string", "multiValued": false, "stored": true },
    { "name": "jew_slug", "type": "string", "multiValued": false, "stored": true },
    { "name": "jew_karat", "type": "string", "multiValued": false, "stored": true },
    { "name": "jew_metal_tone", "type": "string", "multiValued": false, "stored": true },
    { "name": "jew_metal_type", "type": "string", "multiValued": false, "stored": true },
    { "name": "jew_metal_weight", "type": "string", "multiValued": false, "stored": true },
    { "name": "jew_origin", "type": "string", "multiValued": false, "stored": true },
    { "name": "jew_tags", "type": "string", "multiValued": true, "stored": true },
    { "name": "jew_sell_price", "type": "pfloat", "multiValued": false, "stored": true },
    { "name": "ring_size", "type": "string", "multiValued": false, "stored": true },
    { "name": "jew_length", "type": "string", "multiValued": false, "stored": true },
    { "name": "dia_stone_type", "type": "string", "multiValued": false, "stored": true },
    { "name": "dia_shape", "type": "string", "multiValued": false, "stored": true },
    { "name": "dia_quality", "type": "string", "multiValued": false, "stored": true },
    { "name": "dia_tdw", "type": "string", "multiValued": false, "stored": true },
    { "name": "jew_currency", "type": "string", "multiValued": false, "stored": true },
    { "name": "jew_status", "type": "string", "multiValued": false, "stored": true },
    { "name": "jew_finish_level", "type": "string", "multiValued": false, "stored": true },
    { "name": "jew_images", "type": "string", "multiValued": true, "stored": true },
    { "name": "jew_videos", "type": "string", "multiValued": true, "stored": true },
    { "name": "jew_props", "type": "string", "multiValued": true, "stored": true },
    { "name": "created_at", "type": "string", "multiValued": false, "stored": true }
  ],
  "add-dynamic-field": [
    { "name": "variation.id.*", "type": "string", "multiValued": false, "stored": true },
    { "name": "variation.karat.*", "type": "string", "multiValued": false, "stored": true },
    { "name": "variation.metal_tone.*", "type": "string", "multiValued": false, "stored": true },
    { "name": "variation.dia_quality.*", "type": "string", "multiValued": false, "stored": true },
    { "name": "variation.price.*", "type": "pfloat", "multiValued": false, "stored": true },
    { "name": "variation.images.*", "type": "string", "multiValued": true, "stored": true },
    { "name": "variation.videos.*", "type": "string", "multiValued": true, "stored": true }
  ]
}
EOF
```

---

## 5️⃣ Add AI Vector Field Support

### Define a custom vector field type:

```bash
curl -X POST -H "Content-Type: application/json" --data-binary '{
  "add-field-type": {
    "name": "custom_vector",
    "class": "solr.DenseVectorField",
    "vectorDimension": 512,
    "similarityFunction": "cosine"
  }
}' "http://localhost:8983/solr/AI_NEW/schema"
```

### Add vector fields:

```bash
curl -X POST -H 'Content-type:application/json' --data-binary '{
  "add-field": [
    { "name": "image_embedding", "type": "custom_vector", "indexed": true, "stored": true },
    { "name": "text_embedding", "type": "custom_vector", "indexed": true, "stored": true }
  ]
}' "http://localhost:8983/solr/AI_NEW/schema"
```

---

## 6️⃣ Post Cleaned Data to AI_NEW Core

```bash
/opt/solr/bin/post -c AI_NEW /var/www/SOLR_AI/clean_docs.json
OR
bin/post -c AI_NEW /var/www/SOLR_AI /clean_docs.json
bin/solr post -c AI_NEW /home/developer/Downloads/clean_docs.json

```

---

## ✅ Done!

You’ve now fully exported, cleaned, and re-imported your Solr dataset into a new AI-ready core.

---
