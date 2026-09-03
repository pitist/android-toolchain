# Guía de migración

## De versión v0.x a v1.0.0

### Cambios importantes
- El monorepo ahora está en `android-toolchain`.
- Los workflows se han unificado en `audit.yml`.
- Se han añadido reglas de seguridad (S127-S132).

### Pasos para migrar
1. Elimina workflows antiguos de tus repositorios.
2. Añade el nuevo `audit.yml`.
3. Actualiza tus scripts locales para usar el monorepo.

## Soporte
- Issues: https://github.com/pitist/android-toolchain/issues
- Documentación: https://github.com/pitist/android-toolchain/docs