from Scripts.componentManager import newComponent


@newComponent
class Collider():
    """Used to check as to whether the selected item is colliding with an object
    This will NOT handle physics, incase it should be used as a collisionless trigger that has an
    activation area. If you want to add physical collisions, use this in tangent with RigidBody
    It works by having a tag or set of tags in which it can collide with"""
    from Scripts.Components.components import Transform
    requiredDependencies={ "Transform": Transform }

    class Hitbox():
        def __init__(self,
                transform,
                offset,
                xLength:int, yLength:int,
                ) -> None:
            self.Transform = transform
            self.collideList = []
            self.xLength = xLength
            self.yLength = yLength

        def check(self, item):
            s = self.Transform
            i = item.Transform
            if  i.yPos +  item.yLength >= s.yPos \
            and i.yPos <= self.yLength +  s.yPos \
            and i.xPos +  item.xLength >= s.xPos \
            and i.xPos <= self.xLength +  s.xPos :
                return True
            return False

    def init(self,
        Transform,
        xLength:int=50, yLength:int=50,
        hitboxs:set|str='BoxCollider',
        collisionTags:set=set(),
        **kwargs) -> None:

        BoxCollider = {
        Collider.Hitbox( #overall
            Transform,
            Transform.Vector(0, 0),
            xLength, yLength
            ),
        Collider.Hitbox( #top
            Transform,
            Transform.Vector(0, 0),
            xLength, yLength/2
            ),
        Collider.Hitbox( #bottom
            Transform,
            Transform.Vector(0, yLength/2),
            xLength, yLength/2
            ),
        Collider.Hitbox( #left
            Transform,
            Transform.Vector(0, 0),
            xLength/2, yLength
            ),
        Collider.Hitbox( #right
            Transform,
            Transform.Vector(xLength/2, 0),
            xLength/2, yLength
            ),
        }

        defaultHitboxTypes = {
            'BoxCollider': BoxCollider
        }

        self.Transform = Transform
        self.xLength = xLength
        self.yLength = yLength
        if isinstance(hitboxs, str):
            if hitboxs in defaultHitboxTypes:
                hitboxs = defaultHitboxTypes[hitboxs]
            else:
                hitboxs = defaultHitboxTypes['BoxCollider']
        else:
            self.hitboxs = hitboxs
        self.collideList: list[tuple[object, list[bool]]] = []
        self.collisionTags=collisionTags

    def update(self) -> None:
        for tag in self.collisionTags:
            for object in self.scene.SceneTags[tag]: # type: ignore
                if not 'Collider' in object.Components: continue
                Colliding = False
                for checkingHitbox in self.hitboxs:
                    for questioningHitbox in object.Collider.hitboxs:
                        if checkingHitbox.check(questioningHitbox):
                            Colliding = True
                            checkingHitbox.collideList.append(questioningHitbox)

                if Colliding:
                    self.collideList.append(object)


@newComponent
class RigidBody():
    """Used to handle collisions, gravity and other physical forces
    Use with a Collider to properly collide with other objects that have Colliders 
    mass = weight of object
    grounded = is touching ground and is unaffected by gravity until leaving ground again. 
    """
    from Scripts.Components.components import Transform
    requiredDependencies={
    "Transform": Transform, "Collider": Collider
    }


    def init(self,
            Transform,
            Collider,
            mass:int=0,

            **kwargs) -> None:
        self.Transform = Transform
        self.Collider = Collider
        self.mass = mass
        self.grounded = True

    def update(self) -> None:
        if not self.grounded:
            if self.Transform.yVel < self.mass:
                self.Transform.yVel += self.mass / 100
                if self.Transform.yVel > self.mass:
                    self.Transform.yVel = self.mass

        self.grounded = False
        for i in self.Collider.collideList:
            item, lis = i
            if lis[1]:
                self.grounded = True
                self.Transform.yVel = 0
                self.Transform.yPos = item.yPos - self.Collider.yLength
            if lis[2]:
                self.Transform.yVel = 0
                self.Transform.yPos = item.yPos + item.Collider.yLength
            if lis[3]:
                self.Transform.xVel = 0
                self.Transform.xPos = item.xPos + self.Collider.xLength
            if lis[4]:
                self.Transform.xVel = 0
                self.Transform.xPos = item.yPos - item.Collider.yLength