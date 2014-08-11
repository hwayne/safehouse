Safehouse fix-architecture-nightmare
===

In my attempt to keep all of the apps decoupled, I accidentally made it impossible to extend the system. For example, there's no way to add an sms command that calls an sms view, because that would create a circular dependency.

Also, everything is still coupled. We have to fix that.

Changes
-

1. Move the contact sms generators to the sms app
2. Remove the entire "internal routes" thingy
3. Place the sms commands directly in the sms app
   * sms will need to pull the Contact model from panic, creating minimal but necessary coupling
4. Rename panic to contact
5. Comment _everything_.
